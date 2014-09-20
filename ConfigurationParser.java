// TO DO..
// This file is in the making.
// This is neither complete nor correct.



public class ConfigurationParser {

private Document document;
private NodeList nodelist;
private Node=null;

private static  ConfigurationParser cParser=null;
private ConfigurationParser(){
}

public static ConfigurationParser getInstance(){
if(cParser==null)cParser=new ConfigurationParser();
return cParser;
}


private String configFile;
public void setConfigFile(String configfile){ this.configFile=configfile;}
public String getConfigFile(){ return configFile;}

private void init(){
  try{
    DocumentBuilderFactory dbf= DocumentBuilderFactory.newInstance();
    DocumentBuilder db=dbf.newDocumentBuilder();
    Document document=db.parse(getConfigFile());
    NodeList nodelist=document.getElementsByTagName("Setting");
  }catch(Exception exp){
    exp.printStackTrace(System.err);
  }
}

public void parse(){
try{
  init();
  if(document ==null ) {
      System.err.println("Something has gone wrong while initializing the document... Cannot continue..");
      System.exit(-1);
  }
  
  if(nodelist ==null ) {
      System.err.println("Something has gone wrong while initializing the document... Cannot continue..");
      System.exit(-1);
  }
  
  

}catch(Exception exp){
  exp.printStackTrace(System.err);
}


}

}
