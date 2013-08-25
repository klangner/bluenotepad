# -*- coding: utf-8 -*-
'''
Created on 24-08-2013

@author: Krzysztof Langner
'''
from sloppy.interpreter import Runtime
import os.path
import unittest

DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'testdata/')
COMMANDS_FILE = os.path.join(os.path.dirname(__file__), 'testdata/commands.txt')

class CommandsMockup(object):
    
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.result = ''
        
    def loadData(self, months):
        self.result = "load " + months.join(', ')
            
    def printEventCount(self):
        self.result = "event count"
    
    def printSessionCount(self):
        self.result = "session count"

    def notRecognized(self):
        self.result = 'not recognized'
        

class Test(unittest.TestCase):

    def testNoCommand(self):
        commands = CommandsMockup(DATA_FOLDER)
        runtime = Runtime(commands)
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
        runtime = Runtime(CommandsMockup(DATA_FOLDER))
        tokens = [('ala', ''), ('ma', ''), ('kota', '')]
        words = [('alexandra', '')]
        self.assertFalse(runtime._contains(tokens, words))

    def testContainsFalse2(self):
        runtime = Runtime(CommandsMockup(DATA_FOLDER))
        tokens = [('ala', ''), ('ma', ''), ('kota', 'NN')]
        words = [('ala', ''), ('kota', 'NA')]
        self.assertFalse(runtime._contains(tokens, words))

    def testContainsTrue(self):
        runtime = Runtime(CommandsMockup(DATA_FOLDER))
        tokens = [('ala', ''), ('ma', ''), ('kota', 'NN')]
        words = [('ala', ''), ('kota', 'NN')]
        self.assertTrue(runtime._contains(tokens, words))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTokenizer1']
    unittest.main()