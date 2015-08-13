#!/usr/bin/python

import unittest
import json
from category_tree import category_tree

class TestCategoryTree(unittest.TestCase):

    def test_recursive_string_key(self):
        ct = category_tree(data='a/b/c', type='recursive')
        self.assertEqual(json.loads(str(ct)), {u"a": {u"b": {u"c": {}}}})

    def test_recursive_list_key(self):
        ct = category_tree(data=["a/b", "a/c/d"], type='recursive')
        self.assertEqual(json.loads(str(ct)),
                         {u"a": {u"c": {u"d": {}}, u"b": {}}})

    def test_recursive_dict_key(self):
        ct = category_tree(data={u"a/b": u"c", u"a/c": [u"d", u"e"]},
                           type='recursive')
        self.assertEqual(json.loads(str(ct)),
                         {u'a': {u'c': {u'e': {}, u'd': {}}, u'b': {u'c': {}}}})

    def test_iterative_string_key(self):
        ct = category_tree(data='a/b/c', type='iterative')
        self.assertEqual(json.loads(str(ct)), {u"a": {u"b": {u"c": {}}}})

    def test_iterative_list_key(self):
        ct = category_tree(data=["a/b", "a/c/d"], type='iterative')
        self.assertEqual(json.loads(str(ct)),
                         {u"a": {u"c": {u"d": {}}, u"b": {}}})

    def test_iterative_dict_key(self):
        ct = category_tree(data={u"a/b": u"c", u"a/c": [u"d", u"e"]},
                           type='iterative')
        self.assertEqual(json.loads(str(ct)),
                         {u'a': {u'c': {u'e': {}, u'd': {}}, u'b': {u'c': {}}}})

if __name__ == '__main__':
    unittest.main()
