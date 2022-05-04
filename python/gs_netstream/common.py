#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by Yoann Pigné on 2011-08-21.
Copyright (c) 2011 University of Luxembourg. All rights reserved.
"""


class AttributeSink:
    def graph_attribute_added(self, source_id, time_id, attribute, value):
        raise NotImplemented

    def graph_attribute_changed(self, source_id, time_id, attribute, old_value, new_value):
        raise NotImplemented

    def graph_attribute_removed(self, source_id, time_id, attribute):
        raise NotImplemented

    def node_attribute_added(self, source_id, time_id, node_id, attribute, value):
        raise NotImplemented

    def node_attribute_changed(self, source_id, time_id, node_id, attribute, old_value, new_value):
        raise NotImplemented

    def node_attribute_removed(self, source_id, time_id, node_id, attribute):
        raise NotImplemented

    def edge_attribute_added(self, source_id, time_id, edge_id, attribute, value):
        raise NotImplemented

    def edge_attribute_changed(self, source_id, time_id, edge_id, attribute, old_value, new_value):
        raise NotImplemented

    def edge_attribute_removed(self, source_id, time_id, edge_id, attribute):
        raise NotImplemented


class ElementSink:
    def node_added(self, source_id, time_id, node_id):
        raise NotImplemented

    def node_removed(self, source_id, time_id, node_id):
        raise NotImplemented

    def edge_added(self, source_id, time_id, edge_id, from_node, to_node, directed):
        raise NotImplemented

    def edge_removed(self, source_id, time_id, edge_id):
        raise NotImplemented

    def step_begun(self, source_id, time_id, timestamp):
        raise NotImplemented

    def graph_cleared(self, source_id, time_id):
        raise NotImplemented
