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
import json
import os.path


class DefaultCommands(object):
    
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.events = []
        
    def _load(self, filename):
        with open(filename, "r") as f:
            for line in f:
                event = json.loads(line)
                self.events.append(event)

    def loadData(self, months):
        for month in months:
            self._load(self.data_folder+month+".log")

    def printEventCount(self):
        print('Events: %d' % len(self.events))
    
    def printSessionCount(self):
        sessions = set()
        for event in self.events:
            sessions.add(event['session'])
        print('Sessions: %d' % len(sessions))
        
    def notRecognized(self, ):
        print('command not recognized')
    
        

class Runtime():
    
    def __init__(self, commands):
        self.commands = commands
            
    def execute(self, command):
        tokens = self._parseCommand(command)
        if self._contains(tokens, ['count', 'events']):
            self.commands.printEventCount()
        elif self._contains(tokens, ['count', 'sessions']):
            self.commands.printSessionCount()
        else:
            self.commands.notRecognized()
            
    def _parseCommand(self, command):
        return tokenize(command.lower())
            
    def _contains(self, tokens, words):
        count = 0
        for word in words:
            for token in tokens:
                if word == token:
                    count += 1
                    break
        return count == len(words)
    

if __name__ == '__main__':
    folder = os.path.join(os.path.dirname(__file__), 'tests/testdata/')
    runtime = Runtime(DefaultCommands(folder))
    runtime.execute('Count sessions')