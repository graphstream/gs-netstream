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

#if !defined(__MINGW32__)
#include <sys/socket.h>
#endif
#include <errno.h>

#include "netstream-sizes.h"
#include "netstream-storage.h"
#include "netstream-socket.h"
#include "netstream-constants.h"

using namespace std;


namespace netstream{
  
class NetStreamSender{

protected:
  GS_STRING _stream_name;
  GS_STRING _host;
  GS_INT _port;
  NetStreamSocket _socket;
  NetStreamStorage _stream;
  GS_BOOL debug;

  void init();
  
  template <typename T>
  GS_INT getType(T t)
  {
    return _getType(t);
  }
  template <typename T>
  GS_INT getType(const vector<T> & t)
  {
    return _getType(t);
  }

  GS_INT _getType(GS_CHAR object);
  GS_INT _getType(GS_BOOL object);
  GS_INT _getType(GS_INT object);
  GS_INT _getType(GS_LONG object);
  GS_INT _getType(GS_FLOAT object);
  GS_INT _getType(GS_DOUBLE object);
  GS_INT _getType(const GS_STRING & object);
  GS_INT _getType( const vector<GS_CHAR> & object);
  GS_INT _getType( const vector<GS_BOOL> & object);
  GS_INT _getType( const vector<GS_INT> & object);
  GS_INT _getType( const vector<GS_LONG> & object);
  GS_INT _getType( const vector<GS_FLOAT> & object);
  GS_INT _getType( const vector<GS_DOUBLE> & object);

  template <typename T>
  void encode(NetStreamStorage & event, const T & value){
    _encode(event, value);
  }
  template <typename T>
  void encode(NetStreamStorage & event, const vector<T> & value){
    _encode(event, value);
  }
  void _encode(NetStreamStorage & event, GS_CHAR value);
  void _encode(NetStreamStorage & event, GS_BOOL value);
  void _encode(NetStreamStorage & event, GS_INT value);
  void _encode(NetStreamStorage & event, GS_LONG value);
  void _encode(NetStreamStorage & event, GS_FLOAT value);
  void _encode(NetStreamStorage & event, GS_DOUBLE value);
  void _encode(NetStreamStorage & event, const GS_STRING & value);
  
  void _encode(NetStreamStorage & event, const vector<GS_CHAR> & value);
  void _encode(NetStreamStorage & event, const vector<GS_BOOL> & value);
  void _encode(NetStreamStorage & event, const vector<GS_INT> & value);
  void _encode(NetStreamStorage & event, const vector <GS_LONG> & value);
  void _encode(NetStreamStorage & event, const vector <GS_FLOAT> & value);
  void _encode(NetStreamStorage & event, const vector <GS_DOUBLE> & value);
  
  
  void _sendEvent(NetStreamStorage &);
  
public:

  // ================
  // = Constructors =
  // ================
  NetStreamSender(const GS_STRING & host, GS_INT port);
  NetStreamSender(GS_INT port);
  NetStreamSender(const GS_STRING & stream, const GS_STRING & host, GS_INT port);
  NetStreamSender(const GS_STRING & stream, const GS_STRING & host, GS_INT port, GS_BOOL debug);

  // ==================
  // = Element events =
  // ================== 
  void addNode(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & node_id);
  void removeNode(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & node_id);
  void addEdge(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & edge_id, const GS_STRING & from_node, const GS_STRING & to_node, GS_BOOL directed);
  void removeEdge(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & edge_id);
  void stepBegins(const GS_STRING & source_id, GS_LONG time_id, GS_DOUBLE timestamp);
  void graphClear(const GS_STRING & source_id, GS_LONG time_id);
  
  // ====================
  // = Attribute events =
  // ====================
  template <typename T>
  void addGraphAttribute(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & attribute, T value){
    NetStreamStorage event = NetStreamStorage();
    event.writeByte(netstream::EVENT_ADD_GRAPH_ATTR);
    event.writeString(source_id);
    event.writeUnsignedVarInt(time_id);
    event.writeString(attribute);
    event.writeByte(getType(value));
    encode(event, value);
   _sendEvent(event);    
  }

  template <typename T1, typename T2>
  void changeGraphAttribute(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & attribute, const T1 & oldValue, const T2 & newValue){
     NetStreamStorage event = NetStreamStorage();
     event.writeByte(EVENT_CHG_GRAPH_ATTR);
     event.writeString(source_id);
     event.writeUnsignedVarInt(time_id);
     event.writeString(attribute);
     event.writeByte(getType(oldValue));
     encode(event, oldValue);
     event.writeByte(getType(newValue));
     encode(event, newValue);
     _sendEvent(event);
  }
  
  void removeGraphAttribute(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & attribute);
  
  template <typename T>
  void addNodeAttribute(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & node_id, const GS_STRING & attribute, const T & value){
    NetStreamStorage event = NetStreamStorage();
    event.writeByte(EVENT_ADD_NODE_ATTR);
    event.writeString(source_id);
    event.writeUnsignedVarInt(time_id);
    event.writeString(node_id);
    event.writeString(attribute);
    event.writeByte(getType(value));
    encode(event, value);
    _sendEvent(event);
  }

  template <typename T1, typename T2>
  void changeNodeAttribute(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & node_id, const GS_STRING & attribute, const T1 & oldValue, const T2 & newValue){
    NetStreamStorage event = NetStreamStorage();
    event.writeByte(EVENT_CHG_NODE_ATTR);
    event.writeString(source_id);
    event.writeUnsignedVarInt(time_id);
    event.writeString(node_id);
    event.writeString(attribute);
    event.writeByte(getType(oldValue));
    encode(event, oldValue);
    event.writeByte(getType(newValue));
    encode(event, newValue);
    _sendEvent(event);
  }
  
  void removeNodeAttribute(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & node_id, const GS_STRING & attribute);
  
  template <typename T>
  void addEdgeAttribute(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & edge_id, const GS_STRING & attribute, const T & value){
    NetStreamStorage event = NetStreamStorage();
    event.writeByte(EVENT_ADD_EDGE_ATTR);
    event.writeString(source_id);
    event.writeUnsignedVarInt(time_id);
    event.writeString(edge_id);
    event.writeString(attribute);
    event.writeByte(getType(value));
    encode(event, value);
    _sendEvent(event);
    
  }

  template <typename T1, typename T2>
  void changeEdgeAttribute(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & edge_id, const GS_STRING & attribute, const T1 & oldValue, const T2 & newValue){
    NetStreamStorage event = NetStreamStorage();
    event.writeByte(EVENT_CHG_EDGE_ATTR);
    event.writeString(source_id);
    event.writeUnsignedVarInt(time_id);
    event.writeString(edge_id);
    event.writeString(attribute);
    event.writeByte(getType(oldValue));
    encode(event, oldValue);
    event.writeByte(getType(newValue));
    encode(event, newValue);
    _sendEvent(event);
  }
  
  void removeEdgeAttribute(const GS_STRING & source_id, GS_LONG time_id, const GS_STRING & edge_id, const GS_STRING & attribute);
  
};

}
#endif
