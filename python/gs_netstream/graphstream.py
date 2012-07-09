#!/usr/bin/env python
# encoding: utf-8
"""
graphstream.py



Created by Yoann Pigné on 2011-08-21.
Copyright (c) 2011 University of Luxembourg. All rights reserved.
"""

import sys
import os
import unittest


class AttributeSink(object):
  def graphAttributeAdded(self, source_id, time_id, attribute, value):
    raise NotImplementedError
  
  def graphAttributeChanged(self, source_id, time_id, attribute, old_value, new_value):
    raise NotImplementedError
  
  def graphAttributeRemoved(self, source_id, time_id, attribute):
    raise NotImplementedError
  
  def nodeAttributeAdded(self, source_id, time_id, node_id, attribute, value):
    raise NotImplementedError
  
  def nodeAttributeChanged(self, source_id, time_id, node_id, attribute, old_value, new_value):
    raise NotImplementedError
  
  def nodeAttributeRemoved(self, source_id, time_id, node_id, attribute):
    raise NotImplementedError
  
  def edgeAttributeAdded(self, source_id, time_id, edge_id, attribute, value):
    raise NotImplementedError
  
  def edgeAttributeChanged(self, source_id, time_id, edge_id, attribute, old_value, new_value):
    raise NotImplementedError
    
  def edgeAttributeRemoved(self, source_id, time_id, edge_id, attribute):
    raise NotImplementedError

class ElementSink(object):
  def nodeAdded(self, source_id, time_id, node_id):
    raise NotImplementedError
  
  def nodeRemoved(self, source_id, time_id, node_id):
    raise NotImplementedError
  
  def edgeAdded(self, source_id, time_id, edge_id, from_node, to_node, directed):
    raise NotImplementedError
  
  def edgeRemoved(self, source_id, time_id, edge_id):
    raise NotImplementedError
  
  def graphCleared(self):
    raise NotImplementedError
  
  def stepBegins(self, source_id, time_id, timestamp):
    raise NotImplementedError
  

