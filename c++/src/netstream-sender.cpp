/**
 *
 *
 * Copyright (c) 2010-2011 University of Luxembourg
 *
 *
 * @file netstream_sender.cc
 * @date 2011-08-22
 *
 * @author Yoann Pigné
 */


#include "netstream-sender.h"


NetStreamSender::NetStreamSender(const string & host, int port):
_stream_name("default"),_host(host),_port(port),_stream(),_socket(host,port),debug(false)  {
  init();
}

NetStreamSender::NetStreamSender(int port):
_stream_name("default"),_host("localhost"),_port(port),_stream(),_socket("localhost",port),debug(false)  {
  init();
}

NetStreamSender::NetStreamSender(const string & stream, const string & host, int port): 
_stream_name(stream),_host(host),_port(port),_stream(),_socket(host,port),debug(false)
{
  init();
}
NetStreamSender::NetStreamSender(const string & stream, const string & host, int port, bool debug): 
_stream_name(stream),_host(host),_port(port),_stream(),_socket(host,port),debug(debug)
{
  init();
}


void NetStreamSender::init() 
{
  _stream.writeString(_stream_name);
  _socket.connect();
}





// ===========================================
// = Values type guess (templates) =
// ===========================================
int NetStreamSender::_getType(char object){
  if(debug){
    cerr<<"NetStreamSernder: _getType : char"<<endl;
  }
  return TYPE_BYTE;
}

int NetStreamSender::_getType(bool object){
if(debug){
  cerr<<"NetStreamSernder: _getType : bool"<<endl;
}
return TYPE_BOOLEAN;}

int NetStreamSender::_getType(int object){
if(debug){
  cerr<<"NetStreamSernder: _getType : int"<<endl;
}
return TYPE_INT;}
int NetStreamSender::_getType(long object){
if(debug){
  cerr<<"NetStreamSernder: _getType : long"<<endl;
}
return TYPE_LONG;}
int NetStreamSender::_getType(float object){
if(debug){
  cerr<<"NetStreamSernder: _getType : float"<<endl;
}
return TYPE_FLOAT;}
int NetStreamSender::_getType(double object){
if(debug){
  cerr<<"NetStreamSernder: _getType : double"<<endl;
}
return TYPE_DOUBLE;}
int NetStreamSender::_getType(const string & object){
if(debug){
  cerr<<"NetStreamSernder: _getType : string"<<endl;
}
return TYPE_STRING;}
int NetStreamSender::_getType(const vector<char> & object){
if(debug){
  cerr<<"NetStreamSernder: _getType : char* "<<endl;
}
return TYPE_BYTE_ARRAY;}

int NetStreamSender::_getType(const vector <bool> & object){
if(debug){
  cerr<<"NetStreamSernder: _getType : bool*"<<endl;
}
return TYPE_BOOLEAN_ARRAY;}
int NetStreamSender::_getType(const vector<int> & object){
if(debug){
  cerr<<"NetStreamSernder: _getType : int*"<<endl;
}
return TYPE_INT_ARRAY;}
int NetStreamSender::_getType(const vector<long> & object){
if(debug){
  cerr<<"NetStreamSernder: _getType : long*"<<endl;
}
return TYPE_LONG_ARRAY;}
int NetStreamSender::_getType(const vector<float> & object){
if(debug){
  cerr<<"NetStreamSernder: _getType : float*"<<endl;
}
return TYPE_FLOAT_ARRAY;}
int NetStreamSender::_getType(const vector <double> & object){
if(debug){
  cerr<<"NetStreamSernder: _getType : double*"<<endl;
}
return TYPE_DOUBLE_ARRAY;}


// =================
// = data encoding =
// =================
void NetStreamSender::_encode(Storage & event, char value){
  event.writeByte((int)value);
}
void NetStreamSender::_encode(Storage & event, bool value){
  event.writeByte(value?1:0);
}
void NetStreamSender::_encode(Storage & event, int value){
  event.writeInt(value);
}
void NetStreamSender::_encode(Storage & event, long value){
  event.writeLong(value);
}
void NetStreamSender::_encode(Storage & event, float value){
  event.writeFloat(value);
}
void NetStreamSender::_encode(Storage & event, double value){
  event.writeDouble(value);
}
void NetStreamSender::_encode(Storage & event,const  string & value){
  event.writeString(value);
}
void NetStreamSender::_encode(Storage & event, const vector<char> & value){
  event.writeInt(value.size());
  for(vector<char>::const_iterator i = value.begin(); i != value.end(); i++){
    event.writeByte((*i));
  }
}
void NetStreamSender::_encode(Storage & event, const vector<bool> & value){
  event.writeInt(value.size());
  for(vector<bool>::const_iterator i = value.begin(); i != value.end(); i++){
    event.writeByte((*i));
  }
}
void NetStreamSender::_encode(Storage & event, const vector<int> & value){
  event.writeInt(value.size());
  for(vector<int>::const_iterator i = value.begin(); i != value.end(); i++){
    event.writeInt((*i));
  }
}
void NetStreamSender::_encode(Storage & event, const vector<long> & value){
  event.writeInt(value.size());
  for(vector<long>::const_iterator i = value.begin(); i != value.end(); i++){
    event.writeLong((*i));
  }  
}
void NetStreamSender::_encode(Storage & event, const vector<float> & value){
  event.writeInt(value.size());
  for(vector<float>::const_iterator i = value.begin(); i != value.end(); i++){
    event.writeFloat((*i));
  }
}
void NetStreamSender::_encode(Storage & event, const vector<double> &  value){
  event.writeInt(value.size());
  for(vector<double>::const_iterator i = value.begin(); i != value.end(); i++){
    event.writeDouble((*i));
  }
}


void NetStreamSender::_sendEvent(Storage & event){
  
  if(debug){
    cout<<event<<endl;
    /*
    for(Storage::StorageType::const_iterator it = event.begin(); it != event.end();){
      cout<<(int)(*it)<<",";
      it++;
    }
    cout<<endl;
    */
  }
  try{
    _socket.sendExact(_stream+event);
  }
  catch (SocketException &e)
  {
    cout << "Error while sending message: " << e.what();
  }
}

// ==================
// = Element events =
// ================== 
void NetStreamSender::addNode(const string & node_id){
  Storage event = Storage();
  event.writeByte(EVENT_ADD_NODE);
  event.writeString(node_id);
  _sendEvent(event);
}
void NetStreamSender::removeNode(const string & node_id){
  Storage event = Storage();
  event.writeByte(EVENT_DEL_NODE);
  event.writeString(node_id);
  _sendEvent(event);
}
void NetStreamSender::addEdge(const string & edge_id, const string & from_node, const string & to_node, bool directed){
  Storage event = Storage();
  event.writeByte(EVENT_ADD_EDGE);
  event.writeString(edge_id);
  event.writeString(from_node);
  event.writeString(to_node);
  event.writeByte(directed?1:0);
  _sendEvent(event);
}
void NetStreamSender::removeEdge(const string & edge_id){
  Storage event = Storage();
  event.writeByte(EVENT_DEL_EDGE);
  event.writeString(edge_id);
  _sendEvent(event);
}
void NetStreamSender::stepBegins(double timestamp){
  Storage event = Storage();
  event.writeByte(EVENT_STEP);
  event.writeDouble(timestamp);
  _sendEvent(event);
}
void NetStreamSender::graphClear(){
  Storage event = Storage();
  event.writeByte(EVENT_CLEARED);
  _sendEvent(event);  
}

// =====================
// = Attributes events =
// ===================== 

void NetStreamSender::removeNodeAttribute(const string & node_id, const string & attribute){
  Storage event = Storage();
  event.writeByte(EVENT_DEL_NODE_ATTR);
  event.writeString(node_id);
  event.writeString(attribute);
  _sendEvent(event);
}
void NetStreamSender::removeGraphAttribute(const string & attribute){
  Storage event = Storage();
  event.writeByte(EVENT_DEL_GRAPH_ATTR);
  event.writeString(attribute);
  _sendEvent(event);
}
void NetStreamSender::removeEdgeAttribute(const string & edge_id, const string & attribute){
  Storage event = Storage();
  event.writeByte(EVENT_DEL_EDGE_ATTR);
  event.writeString(edge_id);
  event.writeString(attribute);
  _sendEvent(event);
}
