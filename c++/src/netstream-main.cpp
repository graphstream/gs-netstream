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

#include "netstream-sizes.h"
#include "netstream-storage.h"
#include "netstream-socket.h"
#include "netstream-constants.h"
#include "netstream-sender.h"

using namespace std;
using namespace netstream;

void events_test();
void types_test();
void example();
void e();
int main (int argc, char const *argv[])
{
  //events_test();
  //types_test();
  example();
  return 0;
}


void e(){
  string source_id="C++_netstream_test";
  GS_LONG time_id=0L;
   NetStreamSender stream("default","localhost",2001,false);
  string n1("node");
  while(1) {
        //stream.changeNodeAttribute(n1,att,old,n);
        stream.addNode(source_id, time_id++, n1);
  }
}


void example(){
  string source_id("C");
  GS_LONG time_id = 127L;
  NetStreamSender stream("default","localhost",2001,false);
  string style("node{fill-mode:plain;fill-color:#567;size:6px;}");
  stream.addGraphAttribute(source_id, time_id++, "stylesheet", style);
  stream.addGraphAttribute(source_id, time_id++, "test", "test");
  stream.changeGraphAttribute(source_id, time_id++, "test", "test",false);
  stream.addGraphAttribute(source_id, time_id++, "ui.antialias", true);
  stream.addGraphAttribute(source_id, time_id++, "layout.stabilization-limit", 0);
  for (int i = 0; i < 500; i++) {
    stringstream n1;
    n1<<i;
    stream.addNode(source_id, time_id++, n1.str());
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
      stream.addEdge(source_id, time_id++, e1.str(), n1.str(), n2.str(), false);
      stream.addEdge(source_id, time_id++, e2.str(), n1.str(), n3.str(), false);
    }
  }
}

void types_test(){
  string source_id="C++_netstream_test";
  GS_LONG time_id=0L;
  NetStreamSender stream("default","localhost",2001,true);
  
  
  stream.addGraphAttribute(source_id, time_id++, "int", (GS_INT)1);
  stream.addGraphAttribute(source_id, time_id++, "float", (GS_FLOAT)1);
  stream.addGraphAttribute(source_id, time_id++, "double", (GS_DOUBLE)1.0);
  stream.addGraphAttribute(source_id, time_id++, "long", (GS_LONG)1);
  stream.addGraphAttribute(source_id, time_id++, "byte", (GS_CHAR)0);
  stream.addGraphAttribute(source_id, time_id++, "boolean", (GS_BOOL)true);

  int v[] = {1776,7,4};
  vector<int> value(v,v+3);
  stream.addGraphAttribute(source_id, time_id++, "intArray", value);
  
  float v2[] = {(float)1776.3,(float)7.3};
  vector<float> value2(v2,v2+2);
  stream.addGraphAttribute(source_id, time_id++, "floatArray", value2);

  double v3[] = {776.3,.3};
  vector<double> value3(v3,v3+2);
  stream.addGraphAttribute(source_id, time_id++, "doubleArray", value3);
  
  GS_LONG v4[] = {1776,7,4};
  vector<GS_LONG> value4(v4,v4+3);
  stream.addGraphAttribute(source_id, time_id++, "longArray", value4);

  GS_CHAR v5[] = {'0',(GS_CHAR)0,'z'};
  vector<GS_CHAR> value5(v5,v5+3);
  stream.addGraphAttribute(source_id, time_id++, "byteArray",value5 );

  bool v6[] = {true,false};
  vector<bool> value6(v6,v6+2);
  stream.addGraphAttribute(source_id, time_id++, "booleanArray", value6);
  
  stream.addGraphAttribute(source_id, time_id++, "string", string("true"));
}

void events_test(){
  string source_id="C++_netstream_test";
  GS_LONG time_id=0L;
  NetStreamSender stream("localhost", 2001);
  stream.addNode(source_id, time_id++, "node0");
  stream.addEdge(source_id, time_id++, "edge", "node0", "node1", true);
  stream.addNodeAttribute(source_id, time_id++, "node0","nodeAttribute", 0);
  stream.changeNodeAttribute(source_id, time_id++, "node0","nodeAttribute",0, 1);
  stream.removeNodeAttribute(source_id, time_id++, "node0","nodeAttribute");
  stream.addEdgeAttribute(source_id, time_id++, "edge","edgeAttribute", 0);
  stream.changeEdgeAttribute(source_id, time_id++, "edge","edgeAttribute", 0,1);
  stream.removeEdgeAttribute(source_id, time_id++, "edge","edgeAttribute");
  stream.addGraphAttribute(source_id, time_id++, "graphAttribute", 0);
  stream.changeGraphAttribute(source_id, time_id++, "graphAttribute", 0, 1);
  stream.removeGraphAttribute(source_id, time_id++, "graphAttribute");
  stream.stepBegins(source_id, time_id++, 1.1);
  stream.removeEdge(source_id, time_id++, "edge");
  stream.removeNode(source_id, time_id++, "node0");
  stream.graphClear(source_id, time_id++);
}

