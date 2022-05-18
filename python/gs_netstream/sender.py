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
from typing import List, Any

from .constants import *
import logging
from random import random
from .common import AttributeSink, ElementSink
from .sender_utils import get_msg, get_type, encode_value


class DefaultNetStreamTransport:
    """Default transport class using TCP/IP networking."""

    def __init__(self, host, port: int):
        """Initialize using host and port."""
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """Connect to remote server if necessary."""
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            logging.info(f"Connected to remote server - host = {self.host}, port = {self.port}")

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
        self.stream_buff = encode_value(stream, TYPE_STRING)

    def set_source_id(self, source_id: str):
        """Set and cache a source ID."""
        self.source_id = source_id
        self.source_id_buff = encode_value(source_id, TYPE_STRING)

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


    # =========================
    # = AttributeSink methods =
    # =========================

    def send_msg(self, source_id: str, values: List[Any], value_types: List[int]):
        if not source_id is self.source_id:
            self.set_source_id(source_id)
        buff = get_msg(values, value_types)
        self.send(buff)

    def node_added(self, source_id: str, time_id: int, node_id: str):
        """A node was added."""
        self.send_msg(source_id=source_id,
                      values=[EVENT_ADD_NODE, source_id, time_id, node_id],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_STRING])
        logging.debug("node added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id
        })

    def node_removed(self, source_id: str, time_id: int, node_id: str):
        """A node was removed."""
        self.send_msg(source_id=source_id,
                      values=[EVENT_DEL_NODE, source_id, time_id, node_id],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_STRING])
        logging.debug("node removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id
        })

    def edge_added(self, source_id: str, time_id: int, edge_id: str, from_node: str, to_node: str, directed: bool):
        """An edge was added."""
        self.send_msg(source_id=source_id,
                      values=[EVENT_ADD_EDGE, source_id, time_id, edge_id, from_node, to_node, directed],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_STRING, TYPE_STRING, TYPE_STRING,
                                   TYPE_BOOLEAN])
        logging.debug("edge added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "edge_id": edge_id,
            "from_node": from_node,
            "to_node": to_node,
            "directed": directed
        })

    def edge_removed(self, source_id: str, time_id: int, edge_id: str):
        """An edge was removed."""
        self.send_msg(source_id=source_id,
                      values=[EVENT_DEL_EDGE, source_id, time_id, edge_id],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_STRING])
        logging.debug("edge removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": edge_id
        })

    def step_begun(self, source_id: str, time_id: int, timestamp: int):
        """A new step begun."""
        self.send_msg(source_id=source_id,
                      values=[EVENT_STEP, source_id, time_id, timestamp],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_DOUBLE])
        logging.debug("step begun: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "timestamp": timestamp
        })

    def graph_cleared(self, source_id: str, time_id: int):
        """The graph was cleared."""
        self.send_msg(source_id=source_id,
                      values=[EVENT_CLEARED, source_id, time_id],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT])
        logging.debug("graph cleared: %s", {
            "source_id": source_id,
            "time_id": time_id
        })

    def graph_attribute_added(self, source_id: str, time_id: int, attribute: str, value):
        """A graph attribute was added."""
        dtype = get_type(value)
        self.send_msg(source_id=source_id,
                      values=[EVENT_ADD_GRAPH_ATTR, source_id, time_id, attribute, dtype, value],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_STRING, TYPE_BYTE, dtype])
        logging.debug("graph attribute added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "attribute": attribute,
            "value": value
        })

    def graph_attribute_changed(self, source_id: str, time_id: int, attribute: str, old_value, new_value):
        """A graph attribute was changed."""
        old_value_dtype = get_type(old_value)
        new_value_dtype = get_type(new_value)

        self.send_msg(source_id=source_id,
                      values=[EVENT_CHG_GRAPH_ATTR, source_id, time_id, attribute, old_value_dtype, old_value,
                              new_value_dtype, new_value],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_STRING, TYPE_BYTE, old_value_dtype,
                                   TYPE_BYTE, new_value_dtype])
        logging.debug("graph attribute changed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "attribute": attribute,
            "old_value": old_value,
            "new_value": new_value
        })

    def graph_attribute_removed(self, source_id: str, time_id: int, attribute: str):
        """A graph attribute was removed."""
        self.send_msg(source_id=source_id,
                      values=[EVENT_DEL_GRAPH_ATTR, source_id, time_id, attribute],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_STRING])
        logging.debug("graph attribute removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "attribute": attribute
        })

    def node_attribute_added(self, source_id: str, time_id: int, node_id: str, attribute: str, value):
        """A node attribute was added."""
        dtype = get_type(value)
        self.send_msg(source_id=source_id,
                      values=[EVENT_ADD_NODE_ATTR, source_id, time_id, node_id, attribute, dtype, value],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_STRING, TYPE_STRING, TYPE_BYTE, dtype])
        logging.debug("node attribute added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id,
            "attribute": attribute,
            "value": value
        })

    def node_attribute_changed(self, source_id: str, time_id: int, node_id: str, attribute: str, old_value, new_value):
        """A node attribute was changed."""
        old_value_dtype = get_type(old_value)
        new_value_dtype = get_type(new_value)

        self.send_msg(source_id=source_id,
                      values=[EVENT_CHG_NODE_ATTR, source_id, time_id, node_id, attribute, old_value_dtype, old_value,
                              new_value_dtype, new_value],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_STRING, TYPE_STRING, TYPE_BYTE,
                                   old_value_dtype, TYPE_BYTE, new_value_dtype])
        logging.debug("node attribute changed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id,
            "attribute": attribute,
            "old_value": old_value,
            "new_value": new_value
        })

    def node_attribute_removed(self, source_id: str, time_id: int, node_id: str, attribute: str):
        """A node attribute was removed."""
        self.send_msg(source_id=source_id,
                      values=[EVENT_DEL_NODE_ATTR, source_id, time_id, node_id, attribute],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_STRING, TYPE_STRING])
        logging.debug("node attribute removed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "node_id": node_id,
            "attribute": attribute
        })

    def edge_attribute_added(self, source_id: str, time_id: int, edge_id: str, attribute: str, value):
        """An edge attribute was added."""
        dtype = get_type(value)
        self.send_msg(source_id=source_id,
                      values=[EVENT_ADD_EDGE_ATTR, source_id, time_id, edge_id, attribute, dtype, value],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_STRING, TYPE_STRING, TYPE_BYTE, dtype])
        logging.debug("edge attribute added: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "edge_id": edge_id,
            "attribute": attribute,
            "value": value
        })

    def edge_attribute_changed(self, source_id: str, time_id: int, edge_id: str, attribute: str, old_value, new_value):
        """An edge attribute was changed."""
        old_value_dtype = get_type(old_value)
        new_value_dtype = get_type(new_value)

        self.send_msg(source_id=source_id,
                      values=[EVENT_CHG_EDGE_ATTR, source_id, time_id, edge_id, attribute, old_value_dtype, old_value,
                              new_value_dtype, new_value],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_STRING, TYPE_STRING, TYPE_BYTE,
                                   old_value_dtype, TYPE_BYTE, new_value_dtype])

        logging.debug("edge attribute changed: %s", {
            "source_id": source_id,
            "time_id": time_id,
            "edge_id": edge_id,
            "attribute": attribute,
            "old_value": old_value,
            "new_value": new_value
        })

    def edge_attribute_removed(self, source_id: str, time_id: int, edge_id: str, attribute: str):
        """An edge attribute was removed."""
        self.send_msg(source_id=source_id,
                      values=[EVENT_DEL_EDGE_ATTR, source_id, time_id, edge_id, attribute],
                      value_types=[TYPE_BYTE, TYPE_STRING, TYPE_INT, TYPE_STRING, TYPE_STRING])

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

    def run_sender_method(self, sender_method, *args, **kwargs):
        sender_method(self.source_id, self.time_id, *args, **kwargs)
        self.time_id += 1

    def add_node(self, node: str):
        """Add a node to the graph."""
        self.run_sender_method(self.sender.node_added, node)

    def remove_node(self, node: str):
        """Remove a node from the graph."""
        self.sender.node_removed(self.source_id, self.time_id, node)
        self.time_id += 1

    def add_edge(self, edge: str, from_node: str, to_node: str, directed: bool = False):
        """Add an edge to the graph."""
        self.sender.edge_added(self.source_id, self.time_id, edge, from_node, to_node, directed)
        self.time_id += 1

    def remove_edge(self, edge: str):
        """Remove an edge from the graph."""
        self.sender.edge_removed(self.source_id, self.time_id, edge)
        self.time_id += 1

    def add_attribute(self, attribute: str, value):
        """Add an attribute to the graph."""
        self.sender.graph_attribute_added(self.source_id, self.time_id, attribute, value)
        self.time_id += 1

    def remove_attribute(self, attribute: str):
        """Remove an attribute from the graph."""
        self.sender.graph_attribute_removed(self.source_id, self.time_id, attribute)
        self.time_id += 1

    def change_attribute(self, attribute: str, old_value, new_value):
        """Change an attribute of the graph."""
        self.sender.graph_attribute_changed(self.source_id, self.time_id, attribute, old_value, new_value)
        self.time_id += 1

    def add_node_attribute(self, node: str, attribute: str, value):
        """Add an attribute to a node."""
        self.sender.node_attribute_added(self.source_id, self.time_id, node, attribute, value)
        self.time_id += 1

    def remove_node_attibute(self, node: str, attribute: str):
        """Remove an attribute from a node."""
        self.sender.node_attribute_removed(self.source_id, self.time_id, node, attribute)
        self.time_id += 1

    def change_node_attribute(self, node: str, attribute: str, old_value, new_value):
        """Change an attribute of a node."""
        self.sender.node_attribute_changed(self.source_id, self.time_id, node, attribute, old_value, new_value)
        self.time_id += 1

    def add_edge_attribute(self, edge: str, attribute: str, value):
        """Add an attribute to an edge."""
        self.sender.edge_attribute_added(self.source_id, self.time_id, edge, attribute, value)
        self.time_id += 1

    def remove_edge_attribute(self, edge: str, attribute: str):
        """Remove an attribute from an edge."""
        self.sender.edge_attribute_removed(self.source_id, self.time_id, edge, attribute)
        self.time_id += 1

    def change_edge_attribute(self, edge: str, attribute: str, old_value, new_value):
        """Change an attribute of an edge."""
        self.sender.edge_attribute_changed(self.source_id, self.time_id, edge, attribute, old_value, new_value)
        self.time_id += 1

    def clear_graph(self):
        """Clear the graph."""
        self.sender.graph_cleared(self.source_id, self.time_id)
        self.time_id += 1

    def step_begins(self, time: int):
        """Begin a step."""
        self.sender.step_begun(self.source_id, self.time_id, time)
        self.time_id += 1
