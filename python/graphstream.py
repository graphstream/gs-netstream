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
  def graphAttributeAdded(self, attribute, value):
    raise NotImplementedError
  
  def graphAttributeChanged(self, attribute, old_value, new_value):
    raise NotImplementedError
  
  def graphAttributeRemoved(self, attribute):
    raise NotImplementedError
  
  def nodeAttributeAdded(self, node_id, attribute, value):
    raise NotImplementedError
  
  def nodeAttributeChanged(self, node_id, attribute, old_value, new_value):
    raise NotImplementedError
  
  def nodeAttributeRemoved(self, node_id, attribute):
    raise NotImplementedError
  
  def edgeAttributeAdded(self, edge_id, attribute, value):
    raise NotImplementedError
  
  def edgeAttributeChanged(self, edge_id, attribute, old_value, new_value):
    raise NotImplementedError
    
  def edgeAttributeRemoved(self, edge_id, attribute):
    raise NotImplementedError

class ElementSink(object):
  def nodeAdded(self, node_id):
    raise NotImplementedError
  
  def nodeRemoved(self, node_id):
    raise NotImplementedError
  
  def edgeAdded(self, edge_id, from_node, to_node, directed):
    raise NotImplementedError
  
  def edgeRemoved(self, edge_id):
    raise NotImplementedError
  
  def graphCleared(self):
    raise NotImplementedError
  
  def stepBegins(self, timestamp):
    raise NotImplementedError

class untitledTests(unittest.TestCase):
  def setUp(self):
    pass


if __name__ == '__main__':
  unittest.main()