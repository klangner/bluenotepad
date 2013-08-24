# -*- coding: utf-8 -*-
'''
Created on 24-08-2013

@author: Krzysztof Langner

Example commands:

print number of sessions
print session count
print last 20 events
'''
from sloppy.nlp import tokenize
import os.path

class CommandsPrinter(object):
    
    def notRecognized(self):
        print('command not recognized')
    
    def printSessionCount(self):
        print('print session count')
        

class Runtime():
    
    def __init__(self, filename, commands=None):
        self.data = None
        if commands:
            self.commands = commands
        else:
            self.commands = CommandsPrinter()
        
    def execute(self, command):
        tokens = tokenize(command)
        if self._contains(tokens, ['print', 'count', 'sessions']):
            self.commands.printSessionCount()
        else:
            self.commands.notRecognized()
            
    def _contains(self, tokens, words):
        return False
    

if __name__ == '__main__':
    filename = os.path.join(os.path.dirname(__file__), 'tests/testdata/data1.log')
    runtime = Runtime(filename)
    runtime.execute('Count events')