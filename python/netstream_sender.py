#!/usr/bin/env python
# encoding: utf-8
"""
netstream_sender.py

This module implements a NetStream Sender

Created by Yoann Pigné on 2011-08-20.
Copyright (c) 2011 University of Luxembourg. All rights reserved.

"""

import socket
import struct
import types
import base64
from graphstream import AttributeSink, ElementSink
from netstream_constants import *

class NetStreamTransport(object):
   """Defines the general behaviour of the class that will be in charge of the actuall data sending"""
   
   def __init__(self, stream, host, port):
      raise NotImplementedError
   def connect(self):
      raise NotImplementedError      
   
class DefaultNetStreamTransport(NetStreamTransport):
   stream="Default"
   host="localhost"
   port=2001
   socket=None
 
   def __init__(self, stream, host, port):
      self.stream = stream
      self.stream_string=struct.pack("!i",len(stream))+stream
      self.host = host
      self.port = port
   
   def connect(self):
     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     self.socket.connect((self.host, self.port))
   
   def send(self, event):
      if(self.socket == None):
         self.connect()
      self.socket.sendall(struct.pack("!i",+len(self.stream_string)+len(event))+self.stream_string+event)
   
   
class Base64NetStreamTransport(NetStreamTransport):
   stream="Default"
   host="localhost"
   port=2001
   socket=None

   def __init__(self, stream, host, port):
      self.stream = stream
      self.stream_string=struct.pack("!i",len(stream))+stream
      self.host = host
      self.port = port

   def connect(self):
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socket.connect((self.host, self.port))

   def send(self, event):
      if(self.socket == None):
         self.connect()
      encoded_msg = base64.b64encode(self.stream_string+event)
      self.socket.sendall(base64.b64encode(struct.pack("!i",len(encoded_msg)))+encoded_msg)



class NetStreamSender(AttributeSink,ElementSink):
  """One client must send to only one identified stream (streamID, host, port)"""

  transport = None
  
  
  def __init__(self, *args, **kwargs):
     """Constructor can be with one NetStreamTransport object OR with 3 args: Stream ID, Host, and port number"""
     if len(args) == 1 and isinstance(args[0], NetStreamTransport):
        print("Initialize from transport object")
        self.init_from_transport(args[0])
     else:
        if len(args) == 3 and isinstance(args[0], types.StringType) and isinstance(args[1], types.StringType) and isinstance(args[2], types.IntType):
           print("Initialize from args")
           self.init_from_args(args[0], args[1], args[2])
        else:
           print("Impossible to Initialize")
           
  def init_from_args(self, stream, host, port):
    self.transport = DefaultNetStreamTransport(stream, host,port)
    self.transport.connect();
    
  def init_from_transport(self,transport):
     self.transport = transport
  
  def encode_string(self, string):
    """Encodes a given string"""
    return struct.pack("!i",len(string))+string
  
  def _getType(self, value):
    is_array = isinstance(value,types.ListType)
    if is_array:
      value = value[0]
    if isinstance(value, types.BooleanType):
      if is_array:
        return TYPE_BOOLEAN_ARRAY
      else:
        return TYPE_BOOLEAN
    elif isinstance(value, types.IntType):
      if is_array:
        return TYPE_INT_ARRAY
      else:
        return TYPE_INT
    elif isinstance(value, types.LongType):
      if is_array:
        return TYPE_LONG_ARRAY
      else:
        return TYPE_LONG
    elif isinstance(value, types.FloatType):
      if is_array:
        return TYPE_DOUBLE_ARRAY
      else:
        return TYPE_DOUBLE
    elif isinstance(value, types.StringType) or isinstance(value, types.UnicodeType):
      return TYPE_STRING
    elif isinstance(value, types.DictType):
      raise NotImplementedError("You tried to send a dictionary through the NetStream Protocol, though it is not yet implemented.")
  
  def _encodeValue(self, value, value_type):
    if TYPE_BOOLEAN == value_type:
      return self._encodeBoolean(value)
    elif TYPE_BOOLEAN_ARRAY == value_type:
      return self._encodeBooleanArray(value)
    elif TYPE_INT == value_type:
      return self._encodeInt(value)
    elif TYPE_INT_ARRAY == value_type:
      return self._encodeIntArray(value)
    elif TYPE_LONG == value_type:
      return self._encodeLong(value)
    elif TYPE_LONG_ARRAY == value_type:
      return self._encodeLongArray(value)
    elif TYPE_DOUBLE == value_type:
      return self._encodeDouble(value)
    elif TYPE_DOUBLE_ARRAY == value_type:
      return self._encodeDoubleArray(value)
    elif TYPE_STRING == value_type:
      return self._encodeString(value);
    return None
  
  def _encodeString(self, value):
    return struct.pack("!i",len(value))+value

  def _encodeDoubleArray(self, value):
    if not isinstance(value, types.ListType) or not isinstance(value[0], types.FloatType):
      raise TypeError("You've specified an incorrect type")
    event = struct.pack("!i",len(value))  
    for v in value:
      if not isinstance(v,types.FloatType):
        raise TypeError("You've specified an incorrect type")
      event = event+struct.pack("!d",v)
    return event

  def _encodeDouble(self, value):
    return struct.pack("!d",value)

  def _encodeLongArray(self, value):
    if not isinstance(value, types.ListType) or not isinstance(value[0], types.LongType):
      raise TypeError("You've specified an incorrect type")
    event = struct.pack("!i",len(value))
    for v in value:
      if not isinstance(v,types.LongType):
        raise TypeError("You've specified an incorrect type")
      event = event+struct.pack("!q",v)
    return event
  
  def _encodeLong(self, value):
    return struct.pack("!q",value)
  
  def _encodeIntArray(self, value):
    if not isinstance(value, types.ListType) or not isinstance(value[0], types.IntType):
      raise TypeError("You've specified an incorrect type")
    event = struct.pack("!i",len(value))
    for v in value:
      if not isinstance(v,types.IntType):
        raise TypeError("You've specified an incorrect type")
      event = event+struct.pack("!i",v)
    return event
  
  def _encodeInt(self, value):
    return struct.pack("!i",value)

  
  def _encodeBooleanArray(self, value):
    if not isinstance(value, types.ListType) or not isinstance(value[0], types.BooleanType):
      raise TypeError("You've specified an incorrect type")
    event = struct.pack("!i",len(value))
    for v in value:
      if not isinstance(v,types.BooleanType):
        raise TypeError("You've specified an incorrect type")
      event = event+struct.pack("!?",v)
    return event
  
  def _encodeBoolean(self, value):
    return struct.pack("!?",value)
  
  def _encodeByte(self, value):
    return struct.pack("!b",value)
  
  
  # =========================
  # = AttributeSink methods =
  # =========================
  def graphAttributeAdded(self, source_id, time_id, attribute, value):
    event= self._encodeByte(EVENT_ADD_GRAPH_ATTR)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeString(attribute)
    type = self._getType(value) 
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(value,type)
    self.transport.send(event)
  
  def graphAttributeChanged(self, source_id, time_id, attribute, old_value, new_value):
    event = self._encodeByte(EVENT_CHG_GRAPH_ATTR)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeString(attribute)
    type = self._getType(old_value)
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(old_value,type)
    type = self._getType(new_value)
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(new_value,type)
    self.transport.send(event)
  
  def graphAttributeRemoved(self, source_id, time_id, attribute):
    event = self._encodeByte(EVENT_DEL_GRAPH_ATTR)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeString(attribute)
    self.transport.send(event)
  
  def nodeAttributeAdded(self, source_id, time_id, node_id, attribute, value):
    event = self._encodeByte(EVENT_ADD_NODE_ATTR)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeString(node_id)
    event = event + self._encodeString(attribute)
    type = self._getType(value)
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(value,type)
    self.transport.send(event)
  
  def nodeAttributeChanged(self, source_id, time_id, node_id, attribute, old_value, new_value):
    event = self._encodeByte(EVENT_CHG_NODE_ATTR)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeString(node_id)
    event = event + self._encodeString(attribute)
    type = self._getType(old_value)
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(old_value,type)
    type = self._getType(new_value)
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(new_value,type)
    self.transport.send(event)
  
  def nodeAttributeRemoved(self, source_id, time_id, node_id, attribute):
    event = self._encodeByte(EVENT_DEL_NODE_ATTR)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeString(node_id)
    event = event + self._encodeString(attribute)
    self.transport.send(event)
  
  def edgeAttributeAdded(self, source_id, time_id, edge_id, attribute, value):
    event = self._encodeByte(EVENT_ADD_EDGE_ATTR)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeString(edge_id)
    event = event + self._encodeString(attribute)
    type = self._getType(value)
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(value,type)
    self.transport.send(event)
  
  def edgeAttributeChanged(self, source_id, time_id, edge_id, attribute, old_value, new_value):
    event = self._encodeByte(EVENT_CHG_EDGE_ATTR)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeString(edge_id)
    event = event + self._encodeString(attribute)
    type = self._getType(old_value)
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(old_value,type)
    type = self._getType(new_value)
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(new_value,type)
    self.transport.send(event)
  
  def edgeAttributeRemoved(self, source_id, time_id, edge_id, attribute):
    event = self._encodeByte(EVENT_DEL_EDGE_ATTR)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeString(edge_id)
    event = event + self._encodeString(attribute)
    self.transport.send(event)
  
  def nodeAdded(self, source_id, time_id, node_id):
    event = self._encodeByte(EVENT_ADD_NODE)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeString(node_id)
    self.transport.send(event)
  
  def nodeRemoved(self, source_id, time_id, node_id):
    event = self._encodeByte(EVENT_DEL_NODE)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeString(node_id)
    self.transport.send(event)
  
  def edgeAdded(self, source_id, time_id, edge_id, from_node, to_node, directed):
    event = self._encodeByte(EVENT_ADD_EDGE)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeString(edge_id)
    event = event + self._encodeString(from_node)
    event = event + self._encodeString(to_node)
    event = event + self._encodeBoolean(directed)
    self.transport.send(event)
  
  def edgeRemoved(self, source_id, time_id, edge_id):
    event = self._encodeByte(EVENT_DEL_EDGE)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeString(edge_id)
    self.transport.send(event)
  
  def graphCleared(self, source_id, time_id):
    event = self._encodeByte(EVENT_CLEARED)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    self.transport.send(event)
  
  def stepBegins(self, source_id, time_id, timestamp):
    event = self._encodeByte(EVENT_STEP)
    event = event + self._encodeString(source_id) + self._encodeLong(time_id)
    event = event + self._encodeDouble(timestamp)
    self.transport.send(event)

def example():
  """docstring for main"""
  
  stream = NetStreamSender(Base64NetStreamTransport("default","localhost",2001))
  
  source_id="xxx"
  time_id=0L
  ss = "node{fill-mode:plain;fill-color:#567;size:6px;}";
  
  stream.graphAttributeAdded(source_id, time_id,"stylesheet", ss);time_id+=1;
  stream.graphAttributeAdded(source_id, time_id,"ui.antialias", True);time_id+=1;
  stream.graphAttributeAdded(source_id, time_id,"test", "foo");time_id+=1;
  stream.graphAttributeChanged(source_id, time_id,"test", "foo", False);time_id+=1;
  stream.graphAttributeAdded(source_id, time_id,"layout.stabilization-limit", 0);time_id+=1;
  for i in range(0,500):
    stream.nodeAdded(source_id, time_id,str(i));time_id+=1;
    if(i>0):
      stream.edgeAdded(source_id, time_id,str(i)+"_"+str(i-1), str(i), str(i-1),False);time_id+=1;
      stream.edgeAdded(source_id, time_id,str(i)+"__"+str(i/2), str(i), str(i/2), False);time_id+=1;

def testEvents():
  source_id="xxx"
  time_id=0L
  stream = NetStreamSender("default","localhost",2001)
  stream.nodeAdded(source_id, time_id, "node0");time_id+=1;
  stream.edgeAdded(source_id, time_id,"edge", "node0", "node1", True);time_id+=1;
  stream.nodeAttributeAdded(source_id, time_id, "node0","nodeAttribute", 0);time_id+=1;
  stream.nodeAttributeChanged(source_id, time_id, "node0","nodeAttribute",0, 1);time_id+=1;
  stream.nodeAttributeRemoved(source_id, time_id, "node0","nodeAttribute");time_id+=1;
  stream.edgeAttributeAdded(source_id, time_id, "edge","edgeAttribute", 0);time_id+=1;
  stream.edgeAttributeChanged(source_id, time_id, "edge","edgeAttribute",0, 1);time_id+=1;
  stream.edgeAttributeRemoved(source_id, time_id, "edge","edgeAttribute");time_id+=1;
  stream.graphAttributeAdded(source_id, time_id, "graphAttribute", 0);time_id+=1;
  stream.graphAttributeChanged(source_id, time_id, "graphAttribute",0, 1);time_id+=1;
  stream.graphAttributeRemoved(source_id, time_id, "graphAttribute");time_id+=1;
  stream.stepBegins(source_id, time_id, 1.1);time_id+=1;
  stream.edgeRemoved(source_id, time_id, "edge");time_id+=1;
  stream.nodeRemoved(source_id, time_id,"node0");time_id+=1;
  stream.graphCleared(source_id, time_id);time_id+=1;

def testTypes():
  source_id="xxx"
  time_id=0L
  nsc = NetStreamSender("default","localhost", 2001)
  nsc.graphAttributeAdded(source_id, time_id, "intArray", [0, 1, 2]);time_id+=1;
  nsc.graphAttributeAdded(source_id, time_id, "doubleArray", [0.0,1.1,2.2]);time_id+=1;
  nsc.graphAttributeAdded(source_id, time_id, "longArray", [0L,1L,2L]);time_id+=1;
  nsc.graphAttributeAdded(source_id, time_id, "booleanArray", [True, False]);time_id+=1;
  nsc.graphAttributeAdded(source_id, time_id, "int", 1);time_id+=1;
  nsc.graphAttributeAdded(source_id, time_id, "double", 1.0);time_id+=1;
  nsc.graphAttributeAdded(source_id, time_id, "long", 1L);time_id+=1;
  nsc.graphAttributeAdded(source_id, time_id, "boolean", True);time_id+=1;
  nsc.graphAttributeAdded(source_id, time_id, "string", "true");time_id+=1;

if __name__ == "__main__":
    example()
