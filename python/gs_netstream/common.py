#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by Yoann Pigné on 2011-08-21.
Copyright (c) 2011 University of Luxembourg. All rights reserved.
"""
from abc import ABC, abstractmethod


class AttributeSink(ABC):
    @abstractmethod
    def graph_attribute_added(self, source_id, time_id, attribute, value):
        pass

    @abstractmethod
    def graph_attribute_changed(self, source_id, time_id, attribute, old_value, new_value):
        pass

    @abstractmethod
    def graph_attribute_removed(self, source_id, time_id, attribute):
        pass

    @abstractmethod
    def node_attribute_added(self, source_id, time_id, node_id, attribute, value):
        pass

    @abstractmethod
    def node_attribute_changed(self, source_id, time_id, node_id, attribute, old_value, new_value):
        pass

    @abstractmethod
    def node_attribute_removed(self, source_id, time_id, node_id, attribute):
        pass

    @abstractmethod
    def edge_attribute_added(self, source_id, time_id, edge_id, attribute, value):
        pass

    @abstractmethod
    def edge_attribute_changed(self, source_id, time_id, edge_id, attribute, old_value, new_value):
        pass

    @abstractmethod
    def edge_attribute_removed(self, source_id, time_id, edge_id, attribute):
        pass


class ElementSink(ABC):
    @abstractmethod
    def node_added(self, source_id, time_id, node_id):
        pass

    @abstractmethod
    def node_removed(self, source_id, time_id, node_id):
        pass

    @abstractmethod
    def edge_added(self, source_id, time_id, edge_id, from_node, to_node, directed):
        pass

    @abstractmethod
    def edge_removed(self, source_id, time_id, edge_id):
        pass

    @abstractmethod
    def step_begun(self, source_id, time_id, timestamp):
        pass

    @abstractmethod
    def graph_cleared(self, source_id, time_id):
        pass
