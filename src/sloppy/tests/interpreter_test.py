# -*- coding: utf-8 -*-
'''
Created on 24-08-2013

@author: Krzysztof Langner
'''
from sloppy.interpreter import Runtime
import os.path
import unittest

DATA_FILE = os.path.join(os.path.dirname(__file__), 'testdata/data1.log')
COMMANDS_FILE = os.path.join(os.path.dirname(__file__), 'testdata/commands.txt')

class CommandsMockup(object):
    
    def __init__(self):
        self.result = ''
        
    def notRecognized(self):
        self.result = 'not recognized'
        
    def printEventCount(self, events):
        self.result = str(len(events))
    
    def printSessionCount(self, events):
        sessions = set()
        for event in events:
            sessions.add(event['session'])
        self.result = str(len(sessions))


class Test(unittest.TestCase):

    def testNoCommand(self):
        commands = CommandsMockup()
        runtime = Runtime(DATA_FILE, commands=commands)
        counter = 0
        with open(COMMANDS_FILE, "r") as commands_file:
            for line in commands_file:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    tokens = line.split('->')
                    self.assertEqual(2, len(tokens))
                    runtime.execute(tokens[0])
                    self.assertEqual(tokens[1].strip(), commands.result)
                    counter += 1
        print('Processed %d commands' % counter)

    def testContainsFalse(self):
        runtime = Runtime(DATA_FILE)
        tokens = ['ala', 'ma', 'kota']
        words = ['alexandra']
        self.assertFalse(runtime._contains(tokens, words))

    def testContainsTrue(self):
        runtime = Runtime(DATA_FILE)
        tokens = ['ala', 'ma', 'kota']
        words = ['ala', 'kota']
        self.assertTrue(runtime._contains(tokens, words))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTokenizer1']
    unittest.main()