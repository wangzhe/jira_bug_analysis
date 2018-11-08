import os
import unittest

from os.path import isfile, join

__author__ = 'Jack'

test_path = os.path.dirname(__file__)
test_modules = ['test.' + f.replace('.py', '') for f in os.listdir(test_path) if
                (isfile(join(test_path, f)) and f.startswith('test') and f.endswith('py'))]
suite = unittest.TestSuite()

for t in test_modules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suite_fn = getattr(mod, 'suite')
        suite.addTest(suite_fn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)
