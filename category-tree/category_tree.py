from collections import defaultdict
import json

def tree(): return defaultdict(tree)

def take_two(crumbs):
    return (crumbs.split('/', 1) + [''])[:2]

class CategoryTree(object):
    '''
    Base class for `CategoryTreeRecursive' and `CategoryTreeIterative'.
    This class serves as a container for a `defaultdict', which can
    recursively add more entries.
    '''
    def __init__(self, data={}):
        '''
        Initializes the tree with given data.  Data may be a string,
        a list or a dictionary.  Whenever data are a string, it is
        treated as a key.  Keys are chains of categories and subcategories
        delimited by slashes.  Whenever data are a list, each list entry
        is treated as a string key.  Whenever data are a dictionary,
        its keys are treated as category keys, and its values may be
        either categories, lists of categories or dictionaries.

        Example data:
        "a/b/c" => {"a": {"b": {"c": {}}}}
        ["a/b", "a/c/d"] => {"a": {"b": {}, "c": {"d": {}}}}
        { "a/b": "c", "a/c": ["d", "e"] } => 
            {"a": {"b": {"c": {}}, "c": {"d": {}, "e": {}}}}
        '''
        self._tree = tree()
        def add_rec(tree, data):
            if isinstance(data, dict):
                for key, value in data.iteritems():
                    if isinstance(value, str):
                        self.add(key + '/' + value, tree)
                    elif isinstance(value, dict):
                        add_rec(self.add(key, tree), value)
                    else:
                        for suffix in value:
                            self.add(key + '/' + suffix, tree)
            elif isinstance(data, str):
                self.add(data, tree)
            else:
                for key in data: self.add(key)
        add_rec(self._tree, data)

    def __str__(self):
        return str(json.dumps(self._tree))

class CategoryTreeRecursive(CategoryTree):
    '''
    This class adds entries recursively to its internal dictionary
    structure.
    '''
    def add(self, key, node=None):
        def adder(node, prev, next):
            if not next: return node[prev]
            else: return adder(node[prev], *take_two(next))
        return adder(node or self._tree, *take_two(key))

class CategoryTreeIterative(CategoryTree):
    '''
    This class adds entries iteratively to its internal dictionary
    structure.
    '''
    def add(self, key, node=None):
        node = node or self._tree
        for crumb in key.split('/'): node = node[crumb]
        return node

def category_tree(data={}, type='recursive'):
    '''
    Factory method. Generates either `CategoryTreeRecursive' or
    `CategoryTreeIterative' objects
    data - See `help(CategoryTree.__init__)' for data format descripion.
    type - a string. Possible values are 'recurisve' or 'iterative'.
    '''
    return { 'recursive': CategoryTreeRecursive,
             'iterative': CategoryTreeIterative }[type](data)
