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
        self._tree = tree()
        for key, value in data.iteritems():
            self.add(key, value)

    def __str__(self):
        return str(json.dumps(self._tree))

class CategoryTreeRecursive(CategoryTree):
    '''
    This class adds entries recursively to its internal dictionary
    structure.
    '''
    def add(self, key, value):
        def adder(node, prev, next):
            if not next:
                node[prev] = value
            else:
                nprev, nnext = take_two(next)
                adder(node[prev], nprev, nnext)
        prev, next = take_two(key)
        adder(self._tree, prev, next)

class CategoryTreeIterative(CategoryTree):
    '''
    This class addes entries iteratively to its internal dictionary
    structure.
    '''
    def add(self, key, value):
        breadcrumbs = key.split('/')
        prefix, last = breadcrumbs[:-1], breadcrumbs[-1]
        node = self._tree
        for crumb in prefix:
            node = node[crumb]
        node[last] = value

def category_tree(data={}, type='recursive'):
    '''
    Factory method. Generates either `CategoryTreeRecursive' or
    `CategoryTreeIterative' object.s
    data - a dictionary. The keys in this dictionary, if they contain
           forward slashes will be interpreted as categories, subcategories,
           sub-subcategories and so on.
    type - a string. Possible values are 'recurisve' or 'iterative'.
    '''
    return { 'recursive': CategoryTreeRecursive,
             'iterative': CategoryTreeIterative }[type](data)
