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
from graphstream import AttributeSink, ElementSink
from netstream_constants import *


class NetStreamSender(AttributeSink,ElementSink):
  """One client must send to only one identified stream (streamID, host, port)"""

  
  stream="Default"
  host="localhost"
  port=2001
  
  
  def __init__(self, stream, host, port):
    """Constructor with a Stream ID, a Host and a port number"""
    super(NetStreamSender, self).__init__()
    self.stream = stream
    self.host = host
    
    self._stream = self._encodeString(stream)
    self._connect()
    
  
  def _connect(self):
    self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._socket.connect((self.host, self.port))
  
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
  
  def _send(self, event):
    self._socket.sendall(struct.pack("!i",+len(self._stream)+len(event))+self._stream+event)
  
  # =========================
  # = AttributeSink methods =
  # =========================
  def graphAttributeAdded(self, attribute, value):
    event= self._encodeByte(EVENT_ADD_GRAPH_ATTR)
    event = event + self._encodeString(attribute)
    type = self._getType(value) 
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(value,type)
    self._send(event)
  
  def graphAttributeChanged(self, attribute, old_value, new_value):
    event = self._encodeByte(EVENT_CHG_GRAPH_ATTR)
    event = event + self._encodeString(attribute)
    type = self._getType(old_value)
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(old_value,type)
    event = event + self._encodeValue(new_value,type)
    self._send(event)
  
  def graphAttributeRemoved(self, attribute):
    event = self._encodeByte(EVENT_DEL_GRAPH_ATTR)
    event = event + self._encodeString(attribute)
    self._send(event)
  
  def nodeAttributeAdded(self, node_id, attribute, value):
    event = self._encodeByte(EVENT_ADD_NODE_ATTR)
    event = event + self._encodeString(node_id)
    event = event + self._encodeString(attribute)
    type = self._getType(value)
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(value,type)
    self._send(event)
  
  def nodeAttributeChanged(self, node_id, attribute, old_value, new_value):
    event = self._encodeByte(EVENT_CHG_NODE_ATTR)
    event = event + self._encodeString(node_id)
    event = event + self._encodeString(attribute)
    type = self._getType(old_value)
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(old_value,type)
    event = event + self._encodeValue(new_value,type)
    self._send(event)
  
  def nodeAttributeRemoved(self, node_id, attribute):
    event = self._encodeByte(EVENT_DEL_NODE_ATTR)
    event = event + self._encodeString(node_id)
    event = event + self._encodeString(attribute)
    self._send(event)
  
  def edgeAttributeAdded(self, edge_id, attribute, value):
    event = self._encodeByte(EVENT_ADD_EDGE_ATTR)
    event = event + self._encodeString(edge_id)
    event = event + self._encodeString(attribute)
    type = self._getType(value)
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(value,type)
    self._send(event)
  
  def edgeAttributeChanged(self, edge_id, attribute, old_value, new_value):
    event = self._encodeByte(EVENT_CHG_EDGE_ATTR)
    event = event + self._encodeString(edge_id)
    event = event + self._encodeString(attribute)
    type = self._getType(old_value)
    event = event + self._encodeByte(type)
    event = event + self._encodeValue(old_value,type)
    event = event + self._encodeValue(new_value,type)
    self._send(event)
  
  def edgeAttributeRemoved(self, edge_id, attribute):
    event = self._encodeByte(EVENT_DEL_EDGE_ATTR)
    event = event + self._encodeString(edge_id)
    event = event + self._encodeString(attribute)
    self._send(event)
  
  def nodeAdded(self, node_id):
    event = self._encodeByte(EVENT_ADD_NODE)
    event = event + self._encodeString(node_id)
    self._send(event)
  
  def nodeRemoved(self, node_id):
    event = self._encodeByte(EVENT_DEL_NODE)
    event = event + self._encodeString(node_id)
    self._send(event)
  
  def edgeAdded(self, edge_id, from_node, to_node, directed):
    event = self._encodeByte(EVENT_ADD_EDGE)
    event = event + self._encodeString(edge_id)
    event = event + self._encodeString(from_node)
    event = event + self._encodeString(to_node)
    event = event + self._encodeBoolean(directed)
    self._send(event)
  
  def edgeRemoved(self, edge_id):
    event = self._encodeByte(EVENT_DEL_EDGE)
    event = event + self._encodeString(edge_id)
    self._send(event)
  
  def graphCleared(self):
    event = self._encodeByte(EVENT_CLEARED)
    self._send(event)
  
  def stepBegins(self, timestamp):
    event = self._encodeByte(EVENT_STEP)
    event = event + self._encodeDouble(timestamp)
    self._send(event)


def example():
  """docstring for main"""
  
  stream = NetStreamSender("default","localhost",2001)
  
  ss = "node{fill-mode:plain;fill-color:#567;size:6px;}";
  
  stream.graphAttributeAdded("stylesheet", ss);
  stream.graphAttributeAdded("ui.antialias", True);
  stream.graphAttributeAdded("layout.stabilization-limit", 0);
  for i in range(0,500):
    stream.nodeAdded(str(i));
    if(i>0):
      stream.edgeAdded(str(i)+"_"+str(i-1), str(i), str(i-1),False)
      stream.edgeAdded(str(i)+"__"+str(i/2), str(i), str(i/2), False)

def testEvents():
  stream = NetStreamSender("default","localhost",2001)
  stream.nodeAdded("node0")
  stream.edgeAdded("edge", "node0", "node1", True)  
  stream.nodeAttributeAdded("node0","nodeAttribute", 0);
  stream.nodeAttributeChanged("node0","nodeAttribute",0, 1);
  stream.nodeAttributeRemoved("node0","nodeAttribute");
  stream.edgeAttributeAdded("edge","edgeAttribute", 0);
  stream.edgeAttributeChanged("edge","edgeAttribute",0, 1);
  stream.edgeAttributeRemoved("edge","edgeAttribute");
  stream.graphAttributeAdded("graphAttribute", 0);
  stream.graphAttributeChanged("graphAttribute",0, 1);
  stream.graphAttributeRemoved("graphAttribute");
  stream.stepBegins(1.1);
  stream.edgeRemoved("edge");
  stream.nodeRemoved("node0");
  stream.graphCleared();

def testTypes():
  nsc = NetStreamSender("default","localhost", 2001)
  nsc.graphAttributeAdded("intArray", [0, 1, 2])
  nsc.graphAttributeAdded("doubleArray", [0.0,1.1,2.2])
  nsc.graphAttributeAdded("longArray", [0L,1L,2L])
  nsc.graphAttributeAdded("booleanArray", [True, False])
  nsc.graphAttributeAdded("int", 1)
  nsc.graphAttributeAdded("double", 1.0)
  nsc.graphAttributeAdded("long", 1L);
  nsc.graphAttributeAdded("boolean", True)
  nsc.graphAttributeAdded("string", "true")

if __name__ == "__main__":
    testTypes()
