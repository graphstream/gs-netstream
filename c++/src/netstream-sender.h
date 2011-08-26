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

#include <iostream>

#include <sys/socket.h>
#include <errno.h>

#include "tcpip/storage.h"
#include "tcpip/socket.h"
#include "netstream-constants.h"

using namespace std;
using namespace tcpip;

class NetStreamSender{

protected:
  string _stream_name;
  string _host;
  int _port;
  Socket _socket;
  Storage _stream;
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
  void encode(Storage & event, const T & value){
    _encode(event, value);
  }
  template <typename T>
  void encode(Storage & event, const vector<T> & value){
    _encode(event, value);
  }
  void _encode(Storage & event, char value);
  void _encode(Storage & event, bool value);
  void _encode(Storage & event, int value);
  void _encode(Storage & event, long value);
  void _encode(Storage & event, float value);
  void _encode(Storage & event, double value);
  void _encode(Storage & event, const string & value);
  
  void _encode(Storage & event, const vector<char> & value);
  void _encode(Storage & event, const vector<bool> & value);
  void _encode(Storage & event, const vector<int> & value);
  void _encode(Storage & event, const vector <long> & value);
  void _encode(Storage & event, const vector <float> & value);
  void _encode(Storage & event, const vector <double> & value);
  
  
  void _sendEvent(Storage &);
  
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
  void addNode(const string & node_id);
  void removeNode(const string & node_id);
  void addEdge(const string & edge_id, const string & from_node, const string & to_node, bool directed);
  void removeEdge(const string & edge_id);
  void stepBegins(double timestamp);
  void graphClear();
  
  // ====================
  // = Attribute events =
  // ====================
  template <typename T>
  void addGraphAttribute(const string & attribute,  T value){
    Storage event = Storage();
    event.writeByte(EVENT_ADD_GRAPH_ATTR);
    event.writeString(attribute);
    event.writeByte(getType(value));
    encode(event, value);
   _sendEvent(event);    
  }

  template <typename T>
  void changeGraphAttribute(const string & attribute, const T oldValue, const T newValue){
     Storage event = Storage();
     event.writeByte(EVENT_CHG_GRAPH_ATTR);
     event.writeString(attribute);
     event.writeByte(getType(newValue));
     encode(event, oldValue);
     encode(event, newValue);
     _sendEvent(event);
  }
  
  void removeGraphAttribute(const string & attribute);
  
  template <typename T>
  void addNodeAttribute(const string & node_id, const string & attribute, const T & value){
    Storage event = Storage();
    event.writeByte(EVENT_ADD_NODE_ATTR);
    event.writeString(node_id);
    event.writeString(attribute);
    event.writeByte(getType(value));
    encode(event, value);
    _sendEvent(event);
  }

  template <typename T>
  void changeNodeAttribute(const string & node_id, const string & attribute, const T & oldValue, const T & newValue){
    Storage event = Storage();
    event.writeByte(EVENT_CHG_NODE_ATTR);
    event.writeString(node_id);
    event.writeString(attribute);
    event.writeByte(getType(newValue));
    encode(event, oldValue);
    encode(event, newValue);
    _sendEvent(event);
  }
  
  void removeNodeAttribute(const string & node_id, const string & attribute);
  
  template <typename T>
  void addEdgeAttribute(const string & edge_id, const string & attribute, const T & value){
    Storage event = Storage();
    event.writeByte(EVENT_ADD_EDGE_ATTR);
    event.writeString(edge_id);
    event.writeString(attribute);
    event.writeByte(getType(value));
    encode(event, value);
    _sendEvent(event);
    
  }

  template <typename T>
  void changeEdgeAttribute(const string & edge_id, const string & attribute, const T & oldValue, const T & newValue){
    Storage event = Storage();
    event.writeByte(EVENT_CHG_EDGE_ATTR);
    event.writeString(edge_id);
    event.writeString(attribute);
    event.writeByte(getType(newValue));
    encode(event, oldValue);
    encode(event, newValue);
    _sendEvent(event);
  }
  
  void removeEdgeAttribute(const string & edge_id, const string & attribute);
  
};
#endif