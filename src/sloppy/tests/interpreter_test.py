# -*- coding: utf-8 -*-
'''
Created on 24-08-2013

@author: Krzysztof Langner
'''
from sloppy.interpreter import Runtime
import os.path
import unittest

COMMANDS_FILE = os.path.join(os.path.dirname(__file__), 'testdata/commands.txt')

PARSER_KEYWORDS = [
                   ['count'],
                   ['events']
                   ]

class CommandsMockup(object):
    
    def __init__(self):
        self.result = ''
        
    def loadData(self, features):
        self.result = "load " + features
            
    def printEventCount(self, features):
        self.result = "event count"
        

class Test(unittest.TestCase):

    def testNoCommand(self):
        runtime = Runtime()
        commands = CommandsMockup()
        for keywords in PARSER_KEYWORDS:
            runtime.parser.add_keywords(keywords)
        runtime.add_mapping([('count', 'KEYWORD'),('event', 'KEYWORD')], commands.printEventCount)
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
        runtime = Runtime()
        tokens = [('ala', ''), ('ma', ''), ('kota', '')]
        words = [('alexandra', '')]
        self.assertFalse(runtime._contains(tokens, words))

    def testContainsFalse2(self):
        runtime = Runtime()
        tokens = [('ala', ''), ('ma', ''), ('kota', 'NN')]
        words = [('ala', ''), ('kota', 'NA')]
        self.assertFalse(runtime._contains(tokens, words))

    def testContainsTrue(self):
        runtime = Runtime()
        tokens = [('ala', ''), ('ma', ''), ('kota', 'NN')]
        words = [('ala', ''), ('kota', 'NN')]
        self.assertTrue(runtime._contains(tokens, words))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTokenizer1']
    unittest.main()