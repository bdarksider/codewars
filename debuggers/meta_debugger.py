import unittest
from functools import wraps

class Debugger(object):
    attribute_accesses = []
    method_calls = []

def methods(clsname, methodname, func):
    Debugger.attribute_accesses.append({
        'action': 'set',
        'class': clsname,
        # 'attribute': ...,
        # 'value': value
    })
    def inner(*args, **kwargs):
        Debugger.method_calls.append({
            'class': eval(clsname),
            'method': methodname,
            'args': args,
            'kwargs': kwargs
        })
        return func(*args, **kwargs)
    return inner

class Meta(type):
    def __new__(cls, clsname, bases, dct):
        transformed_attr = {}
        for name, val in sorted(dct.items()):
            # Add all the methods
            
            transformed_attr[name] = methods(clsname, name, val)
            

            # if callable(val) and name != '__metaclass__':
            #     transformed_attr[name] = methods(clsname, name, val)
            # else:
            #     transformed_attr[name] = val

        return super(Meta, cls).__new__(cls, clsname, bases, transformed_attr)


class Foo(object):
    __metaclass__ = Meta
    a = 2
    def __init__(self, x):
        self.x = x

    def bar(self, v):
        return (self.x, v)

class MyTest(unittest.TestCase):
    def test(self):
        a = Foo(1)
        a.bar(2)
        a.c = 2

        calls = Debugger.method_calls

        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0]['args'], (a, 1))
        self.assertEqual(calls[1]['args'], (a, 2))

        # accesses = Debugger.attribute_accesses

        # self.assertEqual(len(accesses), 3)

        # self.assertEqual(accesses[0]['action'], 'set')
        # self.assertEqual(accesses[0]['attribute'], 'x')
        # self.assertEqual(accesses[0]['value'], 1)

        # self.assertEqual(accesses[1]['action'], 'get')
        # self.assertEqual(accesses[1]['attribute'], 'bar')

        # self.assertEqual(accesses[2]['action'], 'get')
        # self.assertEqual(accesses[2]['attribute'], 'x')

if __name__ == '__main__':
    unittest.main()