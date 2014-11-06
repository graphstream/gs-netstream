/**
*
*
* Copyright (c) 2010-2011 University of Luxembourg
*
*
* @file netstream_sender.h
* @date 2011-08-21
*
* @author Yoann Pigné
*/

#ifndef NETSTREAM_SENDER_H
#define NETSTREAM_SENDER_H




#ifndef WIN32
  #include <unistd.h>
#else
  #include <windows.h>
#endif


#include <iostream>

#include "netstream-storage.h"
#include "netstream-socket.h"
#include "netstream-constants.h"

using namespace std;


namespace netstream{
  
class NetStreamSender{

protected:
  string _stream_name;
  string _host;
  int _port;
  NetStreamSocket _socket;
  NetStreamStorage _stream;
  bool debug;

  void init();
  
  template <typename T>
  int getType(T t) 
  {
    return _getType(t);
  }
  template <typename T>
  int getType(const vector<T> & t) 
  {
    return _getType(t);
  }

  int _getType(char object);
  int _getType(bool object);
  int _getType(int object);
  int _getType(long object);
  int _getType(float object);
  int _getType(double object);
  int _getType(const string & object);
  int _getType( const vector<char> & object);
  int _getType( const vector<bool> & object);
  int _getType( const vector<int> & object);
  int _getType( const vector<long> & object);
  int _getType( const vector<float> & object);
  int _getType( const vector<double> & object);

  template <typename T>
  void encode(NetStreamStorage & event, const T & value){
    _encode(event, value);
  }
  template <typename T>
  void encode(NetStreamStorage & event, const vector<T> & value){
    _encode(event, value);
  }
  void _encode(NetStreamStorage & event, char value);
  void _encode(NetStreamStorage & event, bool value);
  void _encode(NetStreamStorage & event, int value);
  void _encode(NetStreamStorage & event, long value);
  void _encode(NetStreamStorage & event, float value);
  void _encode(NetStreamStorage & event, double value);
  void _encode(NetStreamStorage & event, const string & value);
  
  void _encode(NetStreamStorage & event, const vector<char> & value);
  void _encode(NetStreamStorage & event, const vector<bool> & value);
  void _encode(NetStreamStorage & event, const vector<int> & value);
  void _encode(NetStreamStorage & event, const vector <long> & value);
  void _encode(NetStreamStorage & event, const vector <float> & value);
  void _encode(NetStreamStorage & event, const vector <double> & value);
  
  
  void _sendEvent(NetStreamStorage &);
  
public:

  // ================
  // = Constructors =
  // ================
  NetStreamSender(const string & host, int port);
  NetStreamSender(int port); 
  NetStreamSender(const string & stream, const string & host, int port);
  NetStreamSender(const string & stream, const string & host, int port, bool debug);
  // ==================
  // = Element events =
  // ================== 
  void addNode(const string & source_id, long time_id, const string & node_id);
  void removeNode(const string & source_id, long time_id, const string & node_id);
  void addEdge(const string & source_id, long time_id, const string & edge_id, const string & from_node, const string & to_node, bool directed);
  void removeEdge(const string & source_id, long time_id, const string & edge_id);
  void stepBegins(const string & source_id, long time_id, double timestamp);
  void graphClear(const string & source_id, long time_id);
  
  // ====================
  // = Attribute events =
  // ====================
  template <typename T>
  void addGraphAttribute(const string & source_id, long time_id, const string & attribute,  T value){
    NetStreamStorage event = NetStreamStorage();
    event.writeByte(netstream::EVENT_ADD_GRAPH_ATTR);
    event.writeString(source_id);
    event.writeUnsignedVarint(time_id);
    event.writeString(attribute);
    event.writeByte(getType(value));
    encode(event, value);
   _sendEvent(event);    
  }

  template <typename T1, typename T2>
  void changeGraphAttribute(const string & source_id, long time_id, const string & attribute, const T1 & oldValue, const T2 & newValue){
     NetStreamStorage event = NetStreamStorage();
     event.writeByte(EVENT_CHG_GRAPH_ATTR);
     event.writeString(source_id);
     event.writeUnsignedVarint(time_id);
     event.writeString(attribute);
     event.writeByte(getType(oldValue));
     encode(event, oldValue);
     event.writeByte(getType(newValue));
     encode(event, newValue);
     _sendEvent(event);
  }
  
  void removeGraphAttribute(const string & source_id, long time_id, const string & attribute);
  
  template <typename T>
  void addNodeAttribute(const string & source_id, long time_id, const string & node_id, const string & attribute, const T & value){
    NetStreamStorage event = NetStreamStorage();
    event.writeByte(EVENT_ADD_NODE_ATTR);
    event.writeString(source_id);
    event.writeUnsignedVarint(time_id);
    event.writeString(node_id);
    event.writeString(attribute);
    event.writeByte(getType(value));
    encode(event, value);
    _sendEvent(event);
  }

  template <typename T1, typename T2>
  void changeNodeAttribute(const string & source_id, long time_id, const string & node_id, const string & attribute, const T1 & oldValue, const T2 & newValue){
    NetStreamStorage event = NetStreamStorage();
    event.writeByte(EVENT_CHG_NODE_ATTR);
    event.writeString(source_id);
    event.writeUnsignedVarint(time_id);
    event.writeString(node_id);
    event.writeString(attribute);
    event.writeByte(getType(oldValue));
    encode(event, oldValue);
    event.writeByte(getType(newValue));
    encode(event, newValue);
    _sendEvent(event);
  }
  
  void removeNodeAttribute(const string & source_id, long time_id, const string & node_id, const string & attribute);
  
  template <typename T>
  void addEdgeAttribute(const string & source_id, long time_id, const string & edge_id, const string & attribute, const T & value){
    NetStreamStorage event = NetStreamStorage();
    event.writeByte(EVENT_ADD_EDGE_ATTR);
    event.writeString(source_id);
    event.writeUnsignedVarint(time_id);
    event.writeString(edge_id);
    event.writeString(attribute);
    event.writeByte(getType(value));
    encode(event, value);
    _sendEvent(event);
    
  }

  template <typename T1, typename T2>
  void changeEdgeAttribute(const string & source_id, long time_id, const string & edge_id, const string & attribute, const T1 & oldValue, const T2 & newValue){
    NetStreamStorage event = NetStreamStorage();
    event.writeByte(EVENT_CHG_EDGE_ATTR);
    event.writeString(source_id);
    event.writeUnsignedVarint(time_id);
    event.writeString(edge_id);
    event.writeString(attribute);
    event.writeByte(getType(oldValue));
    encode(event, oldValue);
    event.writeByte(getType(newValue));
    encode(event, newValue);
    _sendEvent(event);
  }
  
  void removeEdgeAttribute(const string & source_id, long time_id, const string & edge_id, const string & attribute);
  
};

}
#endif