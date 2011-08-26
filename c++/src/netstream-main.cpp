/**
*
*
* Copyright (c) 2010-2011 University of Luxembourg
*
*
* @file netstream_main.cc
* @date 2011-08-22
*
* @author Yoann Pigné
*/


#include <iostream>
#include <sstream>
#include "tcpip/storage.h"
#include "tcpip/socket.h"
#include "netstream-constants.h"
#include "netstream-sender.h"

using namespace tcpip;
using namespace std;

void events_test();
void types_test();
void example();
int main (int argc, char const *argv[])
{
  //events_test();
  //types_test();
  example();
  return 0;
}




void example(){
  NetStreamSender stream("default","localhost",2001,false);
  string style("node{fill-mode:plain;fill-color:#567;size:6px;}");
  stream.addGraphAttribute("stylesheet", style);
  stream.addGraphAttribute("ui.antialias", true);
  stream.addGraphAttribute("layout.stabilization-limit", 0);
  for (int i = 0; i < 500; i++) {
    stringstream n1;
    n1<<i;
  stream.addNode(n1.str());
  if (i > 0) {
    
    
    stringstream n2;
    n2<<(i-1);
    
    stringstream n3;
    n3<<(i/2);
    
    stringstream e1;
    e1<<n1.str()<<"-"<<n2.str();
    stringstream e2;
    e2<<n1.str()<<"-"<<n3.str();
    //cout<<"edge :"<<e1.str()<<endl;
    stream.addEdge(e1.str(), n1.str(), n2.str(), false);
    stream.addEdge(e2.str(), n1.str(), n3.str(), false);
  }
  }
}

void types_test(){
  NetStreamSender stream("default","localhost",2001,true);
  
  
  stream.addGraphAttribute("int", 1);
  stream.addGraphAttribute("float", (float)1);
  stream.addGraphAttribute("double", 1.0);
  stream.addGraphAttribute("long", 1L);
  stream.addGraphAttribute("byte", (char) 0);
  stream.addGraphAttribute("boolean", true);

  int v[] = {1776,7,4};
  vector<int> value(v,v+3);
  stream.addGraphAttribute("intArray", value);
  
  float v2[] = {(float)1776.3,(float)7.3};
  vector<float> value2(v2,v2+2);
  stream.addGraphAttribute("floatArray", value2);

  double v3[] = {776.3,.3};
  vector<double> value3(v3,v3+2);
  stream.addGraphAttribute("doubleArray", value3);
  
  long int v4[] = {1776,7,4};
  vector<long int> value4(v4,v4+3);
  stream.addGraphAttribute("longArray", value4);

  char v5[] = {'0',(char)0,'z'};
  vector<char> value5(v5,v5+3);
  stream.addGraphAttribute("byteArray",value5 );

  bool v6[] = {true,false};
  vector<bool> value6(v6,v6+2);
  stream.addGraphAttribute("booleanArray", value6);
  
  stream.addGraphAttribute("string", string("true"));
}

void events_test(){
  
  NetStreamSender stream("localhost", 2001);
  stream.addNode("node0");
  stream.addEdge("edge", "node0", "node1", true);
  stream.addNodeAttribute("node0","nodeAttribute", 0);
  stream.changeNodeAttribute("node0","nodeAttribute",0, 1);
  stream.removeNodeAttribute("node0","nodeAttribute");
  stream.addEdgeAttribute("edge","edgeAttribute", 0);
  stream.changeEdgeAttribute("edge","edgeAttribute", 0,1);
  stream.removeEdgeAttribute("edge","edgeAttribute");
  stream.addGraphAttribute("graphAttribute", 0);
  stream.changeGraphAttribute("graphAttribute", 0, 1);
  stream.removeGraphAttribute("graphAttribute");
  stream.stepBegins(1.1);
  stream.removeEdge("edge");
  stream.removeNode("node0");
  stream.graphClear();
}

void crapy_test(){
   //NetStreamSender stream =  NetStreamSender("default","localhost",2001);
   //stream.nodeAdded("node");

  string stream = "default";
  
  Socket socket = Socket("localhost",2001);

  Storage _stream = Storage();
  _stream.writeString(stream);

  try
  {
    socket.connect();
  }
  catch (tcpip::SocketException &e)
  {
    cout << "#Error while connecting: " << e.what();
    return ;
  }

  Storage event = Storage();
  event.writeByte(EVENT_ADD_NODE);
  event.writeString("node0");
  
  //Storage all = Storage();
  //all.writeStorage(_stream);
  //all.writeStorage(event);
  //cout.setf ( ios::hex, ios::basefield );       // set hex as the basefield
  //cout.setf ( ios::showbase );                  // activate showbase
  for(Storage::StorageType::const_iterator it = event.begin(); it != event.end();){
    cout<<(int)(*it)<<",";
    it++;
  }
  cout<<endl;
  try
     {
       socket.sendExact(_stream+event);
     }
     catch (SocketException &e)
     {
       cout << "Error while sending command: " << e.what();
       return ;
     }

  socket.close();
  
}