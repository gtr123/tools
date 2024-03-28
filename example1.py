#Author : Thulasiram G
#Version: 0.01
#Description: This is a script to make IDCS REST API calls asynchronously.
#Basic idea is to capture the HTTP calls in a Json Array and send them asynchronously.


from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)
import grequests,json,sys
import requests

responses=[]
counter={'count':0}

def save(array,filename):
     f=open(filename,'w')
     f.write(json.dumps(array,indent=2))
     f.close()

def print_response(response, *args, **kwargs):
    counter['count'] += 1
    print ('Processed ' + str(counter['count']) +"/" + str(counter['totalCalls']))
    return response


def fetch_access_token(envfile):
    access_token=None
    try:
        env=json.load(open(envfile))
        body="grant_type=client_credentials&scope=urn:opc:idm:__myscopes__"
        response=requests.post(env['url'],auth=(env['id'],env['secret']),headers={"Content-Type":"application/x-www-form-urlencoded"},data=body)
        access_token=response.json()['access_token']
    except Exception as exp:
        print(exp)
    finally:
        return access_token



def makeCalls(token,calls,responsefile,size):
    headers={"Authorization":"Bearer "+token,"Content-Type":"application/json"}
    requests=[]
    validcalls=[]
    invalidcalls=[]

    required_keys={'method','data','url'}
    for call in calls:
        if(set(call.keys()).intersection(required_keys) == required_keys):
            validcalls.append(call)
        else:
            print("Array item does not contain all the required info to make an Admin Rest call")
            invalidcalls.append(call)
            print(json.dumps(call,indent=2))

    print("The total number of valid calls passed in the input: " + str(len(validcalls)))
    print("The total number of calls rejected in the input: " + str(len(invalidcalls)))

    for call in validcalls:
        if(call.get('data') == None):
            requests.append(grequests.request(call['method'],call['url'],headers=headers))
        else:
            requests.append(grequests.request(call['method'],call['url'],json=call.get('data'),headers=headers,hooks={'response':print_response}))       

    rs=tuple(requests)
    reqs=grequests.map(rs,size=size)
    errors=""
    for response in reqs:
        try:
           if response is not None:
               url=response.request.url
               content=response.json()
               content['request-url']=url
               responses.append(content)
        except Exception as exp:
            errors+=(response.text + "\n\n\n")
            print(response.text)
    save(responses,responsefile)
    open("errors_"+outfile,'w').write(errors)
    

config={}

def usage():
    print("Usage: python3 mkCalls.py <infile.json> <outfile.json> <config.json>")
    print("where..")
    print("1. infile.json is the path to a file containing an array of Calls")
    print("   Each call contains a minimum of following fields to consider valid")
    print("   method=[GET|POST|PATCH|PUT|DELETE|HEAD]")
    print("   url=https://<idcs-stripe/admin/v1/...")
    print("   data=An appropriate json payload")
    print("2. outfile.json is the path to a file for storing responses")
    print("3. config.json which is a file containing the connection details")
    print("   url, id and secret fields are expected")

try:
    infile=sys.argv[1]
    outfile=sys.argv[2]
    config=sys.argv[3]
except Exception as exp:
    print(exp)
    usage()
    sys.exit(-1)

if (len(sys.argv) != 4):
    print('Wrong number of arguments passed')
    usage()
    sys.exit(-1)


token=fetch_access_token(config)

try:
    calls=json.load(open(infile))
    counter['totalCalls']=len(calls)
except Exception as exp:
    print (exp)
    calls=None

if token != None and calls != None:
    makeCalls(token,calls,outfile,50)
else:
    print('Error fetching the access token or the file passed is not a json array. Please review.')
