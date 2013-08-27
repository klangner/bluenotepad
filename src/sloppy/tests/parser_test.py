# -*- coding: utf-8 -*-
'''
Created on 24-08-2013

@author: Krzysztof Langner
'''
from sloppy.interpreter import Parser
import os.path
import unittest

COMMANDS_FILE = os.path.join(os.path.dirname(__file__), 'testdata/parser.tests')

class Test(unittest.TestCase):

    def testTokenizer(self):
        parser = Parser()
        tokens = parser._tokenize('count events')
        self.assertEqual(2, len(tokens))
        self.assertEqual([('count', ''), ('events', '')], tokens)

    def testTokenizerWithName(self):
        parser = Parser()
        tokens = parser._tokenize('count "Page loaded" events')
        self.assertEqual(3, len(tokens))
        self.assertEqual(('page loaded', 'NAME'), tokens[1])

    def testStem(self):
        parser = Parser()
        tokens = parser._stem_tokens([('objects', ''), ('events', 'NAME')])
        self.assertEqual([('object', ''), ('events', 'NAME')], tokens)

    def testParser(self):
        counter = 0
        with open(COMMANDS_FILE, "r") as commands_file:
            for line in commands_file:
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    tokens = line.split('|')
                    self.assertEqual(3, len(tokens))
                    parser = Parser()
                    for action_list in tokens[0].split(';'):
                        parser.add_keywords(action_list.split(','))
                    print parser.keywords
                    features = parser.parse(tokens[1])
                    self.assertEqual(tokens[2].strip(), str(features))
                    counter += 1
        print('Parsed %d commands' % counter)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTokenizer1']
    unittest.main()