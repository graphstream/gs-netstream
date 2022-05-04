#!/usr/bin/env python
# encoding: utf-8
"""
sender.py

This module implements a NetStream Sender

Created by Yoann Pigné on 2011-08-20.
Copyright (c) 2011 University of Luxembourg. All rights reserved.

Heavily modified to work with new GraphStream core versions.
Hugo Hromic <hugo.hromic@insight-centre.org>
"""

import socket
import struct
from . import varint
from .constants import *
import logging
from random import random
from .common import AttributeSink, ElementSink


class DefaultNetStreamTransport:
    """Default transport class using TCP/IP networking."""

    def __init__(self, host, port):
        """Initialize using host and port."""
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """Connect to remote server if necessary."""
        if not self.socket:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            logging.info("connected to remote server")

    def send(self, data):
        """Send data to remote server."""
        if not self.socket:
            self.connect()
        try:
            self.socket.sendall(data)
        except socket.error as err:
            self.socket = None
            logging.error(err)

    def close(self):
        """Close the connection."""
        if self.socket:
            self.socket.close()
            self.socket = None
            logging.info("disconnected from remote server")


class NetStreamSender(AttributeSink, ElementSink):
    """One client must send to only one identified stream (streamID, host, port)"""

    def __init__(self, port, host="localhost", stream="default"):
        """Initialize using port, host (optional) and stream ID (optional)."""
        self.host = host
        self.port = port
        self.stream = None
        self.stream_buff = None
        self.set_stream(stream)
        self.source_id = None
        self.source_id_buff = None
        self.set_source_id("")
        self.transport = None
        self.connect()

    def set_stream(self, stream):
        """Set and cache a stream ID."""
        self.stream = stream
        self.stream_buff = self.encode_string(stream)

    def set_source_id(self, source_id):
        """Set and cache a source ID."""
        self.source_id = source_id
        self.source_id_buff = self.encode_string(source_id)

    def connect(self):
        """Connect to the underlying transport."""
        self.transport = DefaultNetStreamTransport(self.host, self.port)

    def send(self, event):
        """Send a graph event to the remote server."""
        packet = bytearray()
        packet.extend(self.stream_buff)
        packet.extend(event)
        buff = bytearray()
        buff.extend(struct.pack("!i", len(packet)))  # fixed 4-bytes size!
        buff.extend(packet)
        self.transport.send(buff)

    def close(self):
        """Close the underlying transport."""
        if self.transport:
            self.transport.close()

    def get_type(self, value):
        """Get the data type for a given value."""
        is_array = isinstance(value, list)
        if is_array:
            value = value[0]
        if isinstance(value, bool):
            if is_array:
                return TYPE_BOOLEAN_ARRAY
            return TYPE_BOOLEAN
        elif isinstance(value, int):
            if is_array:
                return TYPE_INT_ARRAY
            return TYPE_INT
        elif isinstance(value, float):
            if is_array:
                return TYPE_DOUBLE_ARRAY
            return TYPE_DOUBLE
        elif isinstance(value, str):
            return TYPE_STRING
        elif isinstance(value, dict):
            raise NotImplementedError("dicts are not supported")

    def encode_value(self, value, dtype):
        """Encode a value according to a given data type."""
        if dtype is TYPE_BOOLEAN:
            return self.encode_boolean(value)
        elif dtype is TYPE_BOOLEAN_ARRAY:
            return self.encode_boolean_array(value)
        elif dtype is TYPE_INT:
            return self.encode_int(value)
        elif dtype is TYPE_INT_ARRAY:
            return self.encode_int_array(value)
        elif dtype is TYPE_LONG:
            return self.encode_long(value)
        elif dtype is TYPE_LONG_ARRAY:
            return self.encode_long_array(value)
        elif dtype is TYPE_DOUBLE:
            return self.encode_double(value)
        elif dtype is TYPE_DOUBLE_ARRAY:
            return self.encode_double_array(value)
        elif dtype is TYPE_STRING:
            return self.encode_string(value)
        return None

    def encode_boolean(self, value):
        """Encode a boolean type."""
        return bytearray([value & 1])

    def encode_boolean_array(self, value):
        """Encode an array of boolean values."""
        if not isinstance(value, list):
            raise TypeError("value is not an array")
        buff = bytearray()
        buff.extend(varint.encode_unsigned(len(value)))
        for elem in value:
            if not isinstance(elem, bool):
                raise TypeError("array element is not a boolean")
            buff.extend(self.encode_boolean(elem))
        return buff

    def encode_int(self, value):
        """Encode an integer type."""
        return varint.encode_unsigned(value)

    def encode_int_array(self, value):
        """Encode an array of integer values."""
        if not isinstance(value, list):
            raise TypeError("value is not an array")
        buff = bytearray()
        buff.extend(varint.encode_unsigned(len(value)))
        for elem in value:
            if not isinstance(elem, int):
                raise TypeError("array element is not an integer")
            buff.extend(self.encode_int(elem))
        return buff

    def encode_long(self, value):
        """Encode a long type."""
        return self.encode_int(value)  # same as int for now

    def encode_long_array(self, value):
        """Encode an array of long values."""
        return self.encode_int_array(value)  # same as int_array for now

    def encode_double(self, value):
        """Encode a double type."""
        return bytearray(struct.pack("!d", value))

    def encode_double_array(self, value):
        """Encode an array of double values."""
        if not isinstance(value, list):
            raise TypeError("value is not an array")
        buff = bytearray()
        buff.extend(varint.encode_unsigned(len(value)))
        for elem in value:
            if not isinstance(elem, float):
                raise TypeError("array element is not a float/double")
            buff.extend(self.encode_double(elem))
        return buff

    def encode_string(self, string):
        """Encode a string type."""
        data = bytearray(string, "UTF-8")
        buff = bytearray()
        buff.extend(varint.encode_unsigned(len(data)))
        buff.extend(data)
        return buff

    def encode_byte(self, value):
        """Encode a byte type."""
        return bytearray([value])

    # =========================
    # = AttributeSink methods =
    # =========================

    def node_added(self, source_id, time_id, node_id):
        """A node was added."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_ADD_NODE))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_string(node_id))
        self.send(buff)
        logging.debug("node added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id
        })

    def node_removed(self, source_id, time_id, node_id):
        """A node was removed."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_DEL_NODE))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_string(node_id))
        self.send(buff)
        logging.debug("node removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id
        })

    def edge_added(self, source_id, time_id, edge_id, from_node, to_node, directed):
        """An edge was added."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_ADD_EDGE))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_string(edge_id))
        buff.extend(self.encode_string(from_node))
        buff.extend(self.encode_string(to_node))
        buff.extend(self.encode_boolean(directed))
        self.send(buff)
        logging.debug("edge added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "edge_id": edge_id,
            "from_node": from_node,
            "to_node": to_node,
            "directed": directed
        })

    def edge_removed(self, source_id, time_id, edge_id):
        """An edge was removed."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_DEL_EDGE))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_string(edge_id))
        self.send(buff)
        logging.debug("edge removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": edge_id
        })

    def step_begun(self, source_id, time_id, timestamp):
        """A new step begun."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_STEP))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_double(timestamp))
        self.send(buff)
        logging.debug("step begun: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "timestamp": timestamp
        })

    def graph_cleared(self, source_id, time_id):
        """The graph was cleared."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_CLEARED))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        self.send(buff)
        logging.debug("graph cleared: %s", {
            "source_id": source_id,
            "time_id": time_id
        })

    def graph_attribute_added(self, source_id, time_id, attribute, value):
        """A graph attribute was added."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_ADD_GRAPH_ATTR))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_string(attribute))
        dtype = self.get_type(value)
        buff.extend(self.encode_byte(dtype))
        buff.extend(self.encode_value(value, dtype))
        self.send(buff)
        logging.debug("graph attribute added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "attribute": attribute,
            "value": value
        })

    def graph_attribute_changed(self, source_id, time_id, attribute, old_value, new_value):
        """A graph attribute was changed."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_CHG_GRAPH_ATTR))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_string(attribute))
        dtype = self.get_type(old_value)
        buff.extend(self.encode_byte(dtype))
        buff.extend(self.encode_value(old_value, dtype))
        dtype = self.get_type(new_value)
        buff.extend(self.encode_byte(dtype))
        buff.extend(self.encode_value(new_value, dtype))
        self.send(buff)
        logging.debug("graph attribute changed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "attribute": attribute,
            "old_value": old_value,
            "new_value": new_value
        })

    def graph_attribute_removed(self, source_id, time_id, attribute):
        """A graph attribute was removed."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_DEL_GRAPH_ATTR))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_string(attribute))
        self.send(buff)
        logging.debug("graph attribute removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "attribute": attribute
        })

    def node_attribute_added(self, source_id, time_id, node_id, attribute, value):
        """A node attribute was added."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_ADD_NODE_ATTR))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_string(node_id))
        buff.extend(self.encode_string(attribute))
        dtype = self.get_type(value)
        buff.extend(self.encode_byte(dtype))
        buff.extend(self.encode_value(value, dtype))
        self.send(buff)
        logging.debug("node attribute added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id,
            "attribute": attribute,
            "value": value
        })

    def node_attribute_changed(self, source_id, time_id, node_id, attribute, old_value, new_value):
        """A node attribute was changed."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_CHG_NODE_ATTR))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_string(node_id))
        buff.extend(self.encode_string(attribute))
        dtype = self.get_type(old_value)
        buff.extend(self.encode_byte(dtype))
        buff.extend(self.encode_value(old_value, dtype))
        dtype = self.get_type(new_value)
        buff.extend(self.encode_byte(dtype))
        buff.extend(self.encode_value(new_value, dtype))
        self.send(buff)
        logging.debug("node attribute changed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id,
            "attribute": attribute,
            "old_value": old_value,
            "new_value": new_value
        })

    def node_attribute_removed(self, source_id, time_id, node_id, attribute):
        """A node attribute was removed."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_DEL_NODE_ATTR))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_string(node_id))
        buff.extend(self.encode_string(attribute))
        self.send(buff)
        logging.debug("node attribute removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id,
            "attribute": attribute
        })

    def edge_attribute_added(self, source_id, time_id, edge_id, attribute, value):
        """An edge attribute was added."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_ADD_EDGE_ATTR))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_string(edge_id))
        buff.extend(self.encode_string(attribute))
        dtype = self.get_type(value)
        buff.extend(self.encode_byte(dtype))
        buff.extend(self.encode_value(value, dtype))
        self.send(buff)
        logging.debug("edge attribute added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "edge_id": edge_id,
            "attribute": attribute,
            "value": value
        })

    def edge_attribute_changed(self, source_id, time_id, edge_id, attribute, old_value, new_value):
        """An edge attribute was changed."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_CHG_EDGE_ATTR))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_string(edge_id))
        buff.extend(self.encode_string(attribute))
        dtype = self.get_type(old_value)
        buff.extend(self.encode_byte(dtype))
        buff.extend(self.encode_value(old_value, dtype))
        dtype = self.get_type(new_value)
        buff.extend(self.encode_byte(dtype))
        buff.extend(self.encode_value(new_value, dtype))
        self.send(buff)
        logging.debug("edge attribute changed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "edge_id": edge_id,
            "attribute": attribute,
            "old_value": old_value,
            "new_value": new_value
        })

    def edge_attribute_removed(self, source_id, time_id, edge_id, attribute):
        """An edge attribute was removed."""
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = bytearray()
        buff.extend(self.encode_byte(EVENT_DEL_EDGE_ATTR))
        buff.extend(self.encode_string(source_id))
        buff.extend(self.encode_long(time_id))
        buff.extend(self.encode_string(edge_id))
        buff.extend(self.encode_string(attribute))
        self.send(buff)
        logging.debug("edge attribute removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "edge_id": edge_id,
            "attribute": attribute
        })


class NetStreamProxyGraph:
    """
    This is a utility class that handles 'source id' and 'time id' synchronization tokens.
    It proposes utile classes that allow to directly send events through the network pipe.
    """

    def __init__(self, sender, source_id=None):
        """Constructor can be with one NetStreamSender object and a source id OR with with 4 args: Source ID, Stream ID, Host, and port number"""
        self.sender = sender
        self.source_id = source_id if source_id else "nss%d" % (1000 * random())
        self.time_id = 0

    def add_node(self, node):
        """Add a node to the graph."""
        self.sender.node_added(self.source_id, self.time_id, node)
        self.time_id += 1

    def remove_node(self, node):
        """Remove a node from the graph."""
        self.sender.node_removed(self.source_id, self.time_id, node)
        self.time_id += 1

    def add_edge(self, edge, from_node, to_node, directed=False):
        """Add an edge to the graph."""
        self.sender.edge_added(self.source_id, self.time_id, edge, from_node, to_node, directed)
        self.time_id += 1

    def remove_edge(self, edge):
        """Remove an edge from the graph."""
        self.sender.edge_removed(self.source_id, self.time_id, edge)
        self.time_id += 1

    def add_attribute(self, attribute, value):
        """Add an attribute to the graph."""
        self.sender.graph_attribute_added(self.source_id, self.time_id, attribute, value)
        self.time_id += 1

    def remove_attribute(self, attribute):
        """Remove an attribute from the graph."""
        self.sender.graph_attribute_removed(self.source_id, self.time_id, attribute)
        self.time_id += 1

    def change_attribute(self, attribute, old_value, new_value):
        """Change an attribute of the graph."""
        self.sender.graph_attribute_changed(self.source_id, self.time_id, attribute, old_value, new_value)
        self.time_id += 1

    def add_node_attribute(self, node, attribute, value):
        """Add an attribute to a node."""
        self.sender.node_attribute_added(self.source_id, self.time_id, node, attribute, value)
        self.time_id += 1

    def remove_node_attibute(self, node, attribute):
        """Remove an attribute from a node."""
        self.sender.node_attribute_removed(self.source_id, self.time_id, node, attribute)
        self.time_id += 1

    def change_node_attribute(self, node, attribute, old_value, new_value):
        """Change an attribute of a node."""
        self.sender.node_attribute_changed(self.source_id, self.time_id, node, attribute, old_value, new_value)
        self.time_id += 1

    def add_edge_attribute(self, edge, attribute, value):
        """Add an attribute to an edge."""
        self.sender.edge_attribute_added(self.source_id, self.time_id, edge, attribute, value)
        self.time_id += 1

    def remove_edge_attribute(self, edge, attribute):
        """Remove an attribute from an edge."""
        self.sender.edge_attribute_removed(self.source_id, self.time_id, edge, attribute)
        self.time_id += 1

    def change_edge_attribute(self, edge, attribute, old_value, new_value):
        """Change an attribute of an edge."""
        self.sender.edge_attribute_changed(self.source_id, self.time_id, edge, attribute, old_value, new_value)
        self.time_id += 1

    def clear_graph(self):
        """Clear the graph."""
        self.sender.graph_cleared(self.source_id, self.time_id)
        self.time_id += 1

    def step_begins(self, time):
        """Begin a step."""
        self.sender.step_begun(self.source_id, self.time_id, time)
        self.time_id += 1
