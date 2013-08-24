# -*- coding: utf-8 -*-
'''
Created on 24-08-2013

@author: Krzysztof Langner
'''
from sloppy.interpreter import Runtime
import os.path
import unittest

DATA_FILE = os.path.join(os.path.dirname(__file__), 'testdata/data1.log')

class CommandsMockup(object):
    
    def __init__(self):
        self.executed_command = ''
        
    def notRecognized(self):
        self.executed_command = 'not recognized'
    
    def printSessionCount(self):
        self.executed_command = 'print session count'


class Test(unittest.TestCase):

    def testNoCommand(self):
        commands = CommandsMockup()
        runtime = Runtime(DATA_FILE, commands=commands)
        runtime.execute('ala ma kota')
        self.assertEqual('not recognized', commands.executed_command)

#    def testSessionCount(self):
#        commands = CommandsMockup()
#        runtime = Runtime(DATA_FILE, commands=commands)
#        runtime.execute('print session count')
#        self.assertEqual('print session count', commands.executed_command)

    def testContainsTrue(self):
        runtime = Runtime(DATA_FILE)
        tokens = ['ala', 'ma', 'kota']
        words = ['alexandra']
        self.assertFalse(runtime._contains(tokens, words))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTokenizer1']
    unittest.main()