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

namespace netstream{
  
NetStreamSender::NetStreamSender(const GS_STRING & host, GS_INT port):
_stream_name("default"),_host(host),_port(port),_stream(),_socket(host,port),debug(false)  {
  init();
}

NetStreamSender::NetStreamSender(GS_INT port):
_stream_name("default"),_host("localhost"),_port(port),_stream(),_socket("localhost",port),debug(false)  {
  init();
}

NetStreamSender::NetStreamSender(const GS_STRING & stream, const GS_STRING & host, GS_INT port):
_stream_name(stream),_host(host),_port(port),_stream(),_socket(host,port),debug(false)
{
  init();
}
NetStreamSender::NetStreamSender(const GS_STRING & stream, const GS_STRING & host, GS_INT port, GS_BOOL debug):
_stream_name(stream),_host(host),_port(port),_stream(),_socket(host,port),debug(debug)
{
  init();
}


void NetStreamSender::init() 
{ 
  _stream.writeString(_stream_name);
  
  int wait_for_server = 1;
  while(wait_for_server){
    try{
      _socket.connect();
      if(wait_for_server > 1)
            std::cout<<std::endl<<"Connection established."<<std::endl;
      wait_for_server = 0;
    } catch(NetStreamSocketException e){
      if(wait_for_server == 1) 
        std::cout<<"No available connection on "<<_host<<":"<<_port<<". Waiting.";
      else
        std::cout<<"."<<std::flush;
      wait_for_server++;
      sleep(1);
    }
  }
}

// ===========================================
// = Values type guess (templates) =
// ===========================================
GS_INT NetStreamSender::_getType(GS_CHAR object){
  if(debug){
    cerr<<"NetStreamSender: _getType : char"<<endl;
  }
  return TYPE_BYTE;
}

GS_INT NetStreamSender::_getType(GS_BOOL object){
if(debug){
  cerr<<"NetStreamSender: _getType : bool"<<endl;
}
return TYPE_BOOLEAN;}

GS_INT NetStreamSender::_getType(GS_INT object){
if(debug){
  cerr<<"NetStreamSender: _getType : int"<<endl;
}
return TYPE_INT;}

GS_INT NetStreamSender::_getType(GS_LONG object){
if(debug){
  cerr<<"NetStreamSender: _getType : long"<<endl;
}
return TYPE_LONG;}

GS_INT NetStreamSender::_getType(GS_FLOAT object){
if(debug){
  cerr<<"NetStreamSender: _getType : float"<<endl;
}
return TYPE_FLOAT;}

GS_INT NetStreamSender::_getType(GS_DOUBLE object){
if(debug){
  cerr<<"NetStreamSender: _getType : double"<<endl;
}
return TYPE_DOUBLE;}

GS_INT NetStreamSender::_getType(const GS_STRING & object){
if(debug){
  cerr<<"NetStreamSender: _getType : string"<<endl;
}
return TYPE_STRING;}

GS_INT NetStreamSender::_getType(const vector<GS_CHAR> & object){
if(debug){
  cerr<<"NetStreamSender: _getType : char* "<<endl;
}
return TYPE_BYTE_ARRAY;}

GS_INT NetStreamSender::_getType(const vector <GS_BOOL> & object){
if(debug){
  cerr<<"NetStreamSender: _getType : bool*"<<endl;
}
return TYPE_BOOLEAN_ARRAY;}

GS_INT NetStreamSender::_getType(const vector<GS_INT> & object){
if(debug){
  cerr<<"NetStreamSender: _getType : int*"<<endl;
}
return TYPE_INT_ARRAY;}

GS_INT NetStreamSender::_getType(const vector<GS_LONG> & object){
if(debug){
  cerr<<"NetStreamSender: _getType : long*"<<endl;
}
return TYPE_LONG_ARRAY;}

GS_INT NetStreamSender::_getType(const vector<GS_FLOAT> & object){
if(debug){
  cerr<<"NetStreamSender: _getType : float*"<<endl;
}
return TYPE_FLOAT_ARRAY;}

GS_INT NetStreamSender::_getType(const vector <GS_DOUBLE> & object){
if(debug){
  cerr<<"NetStreamSender: _getType : double*"<<endl;
}
return TYPE_DOUBLE_ARRAY;}


// =================
// = data encoding =
// =================
void NetStreamSender::_encode(NetStreamStorage & event, GS_CHAR value){
  event.writeByte((GS_INT)value);
}

void NetStreamSender::_encode(NetStreamStorage & event, GS_BOOL value){
  event.writeByte(value?1:0);
}

void NetStreamSender::_encode(NetStreamStorage & event, GS_INT value){
  event.writeInt(value);
}

void NetStreamSender::_encode(NetStreamStorage & event, GS_LONG value){
  event.writeLong(value);
}

void NetStreamSender::_encode(NetStreamStorage & event, GS_FLOAT value){
  event.writeFloat(value);
}

void NetStreamSender::_encode(NetStreamStorage & event, GS_DOUBLE value){
  event.writeDouble(value);
}

void NetStreamSender::_encode(NetStreamStorage & event, const GS_STRING & value){
  event.writeString(value);
}

void NetStreamSender::_encode(NetStreamStorage & event, const vector<GS_CHAR> & value){
  event.writeInt(value.size());
  for(vector<char>::const_iterator i = value.begin(); i != value.end(); i++){
    event.writeByte((*i));
  }
}

void NetStreamSender::_encode(NetStreamStorage & event, const vector<GS_BOOL> & value){
  event.writeInt(value.size());
  for(vector<bool>::const_iterator i = value.begin(); i != value.end(); i++){
    event.writeByte((*i));
  }
}

void NetStreamSender::_encode(NetStreamStorage & event, const vector<GS_INT> & value){
  event.writeInt(value.size());
  for(vector<int>::const_iterator i = value.begin(); i != value.end(); i++){
    event.writeInt((*i));
  }
}

void NetStreamSender::_encode(NetStreamStorage & event, const vector<GS_LONG> & value){
  event.writeInt(value.size());
  for(vector<GS_LONG>::const_iterator i = value.begin(); i != value.end(); i++){
    event.writeLong((*i));
  }  
}

void NetStreamSender::_encode(NetStreamStorage & event, const vector<GS_FLOAT> & value){
  event.writeInt(value.size());
  for(vector<GS_FLOAT>::const_iterator i = value.begin(); i != value.end(); i++){
    event.writeFloat((*i));
  }
}

void NetStreamSender::_encode(NetStreamStorage & event, const vector<GS_DOUBLE> &  value){
  event.writeInt(value.size());
  for(vector<GS_DOUBLE>::const_iterator i = value.begin(); i != value.end(); i++){
    event.writeDouble((*i));
  }
}


void NetStreamSender::_sendEvent(NetStreamStorage & event){
  
  if(debug){
    cout<<event<<endl;
  }
  try{
    _socket.sendExact(_stream+event);
  }
  catch (NetStreamSocketException &e)
  {
    cout << "Error while sending message: " << e.what();
  }
}

// ==================
// = Element events =
// ================== 
void NetStreamSender::addNode(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & node_id){
  NetStreamStorage event = NetStreamStorage();
  event.writeByte(EVENT_ADD_NODE);
  event.writeString(source_id);
  event.writeUnsignedVarInt(time_id);
  event.writeString(node_id);
  _sendEvent(event);
}

void NetStreamSender::removeNode(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & node_id){
  NetStreamStorage event = NetStreamStorage();
  event.writeByte(EVENT_DEL_NODE);
  event.writeString(source_id);
  event.writeUnsignedVarInt(time_id);
  event.writeString(node_id);
  _sendEvent(event);
}

void NetStreamSender::addEdge(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & edge_id, const GS_STRING & from_node, const GS_STRING & to_node, GS_BOOL directed){
  NetStreamStorage event = NetStreamStorage();
  event.writeByte(EVENT_ADD_EDGE);
  event.writeString(source_id);
  event.writeUnsignedVarInt(time_id);
  event.writeString(edge_id);
  event.writeString(from_node);
  event.writeString(to_node);
  event.writeByte(directed?1:0);
  _sendEvent(event);
}

void NetStreamSender::removeEdge(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & edge_id){
  NetStreamStorage event = NetStreamStorage();
  event.writeByte(EVENT_DEL_EDGE);
  event.writeString(source_id);
  event.writeUnsignedVarInt(time_id);
  event.writeString(edge_id);
  _sendEvent(event);
}

void NetStreamSender::stepBegins(const GS_STRING & source_id, GS_LONG time_id, GS_DOUBLE timestamp){
  NetStreamStorage event = NetStreamStorage();
  event.writeByte(EVENT_STEP);
  event.writeString(source_id);
  event.writeUnsignedVarInt(time_id);
  event.writeDouble(timestamp);
  _sendEvent(event);
}

void NetStreamSender::graphClear(const GS_STRING & source_id, GS_LONG time_id){
  NetStreamStorage event = NetStreamStorage();
  event.writeByte(EVENT_CLEARED);
  event.writeString(source_id);
  event.writeUnsignedVarInt(time_id);
  _sendEvent(event);  
}

// =====================
// = Attributes events =
// ===================== 

void NetStreamSender::removeNodeAttribute(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & node_id, const GS_STRING & attribute){
  NetStreamStorage event = NetStreamStorage();
  event.writeByte(EVENT_DEL_NODE_ATTR);
  event.writeString(source_id);
  event.writeUnsignedVarInt(time_id);
  event.writeString(node_id);
  event.writeString(attribute);
  _sendEvent(event);
}

void NetStreamSender::removeGraphAttribute(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & attribute){
  NetStreamStorage event = NetStreamStorage();
  event.writeByte(EVENT_DEL_GRAPH_ATTR);
  event.writeString(source_id);
  event.writeUnsignedVarInt(time_id);
  event.writeString(attribute);
  _sendEvent(event);
}

void NetStreamSender::removeEdgeAttribute(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & edge_id, const GS_STRING & attribute){
  NetStreamStorage event = NetStreamStorage();
  event.writeByte(EVENT_DEL_EDGE_ATTR);
  event.writeString(source_id);
  event.writeUnsignedVarInt(time_id);
  event.writeString(edge_id);
  event.writeString(attribute);
  _sendEvent(event);
}

}

