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
    
    def notRecognized(self):
        print('command not recognized')
    
    def printEventCount(self, events):
        print('Events: %d' % len(events))
    
    def printSessionCount(self, events):
        sessions = set()
        for event in events:
            sessions.add(event['session'])
        print('Sessions: %d' % len(sessions))
        

class Runtime():
    
    def __init__(self, filename, commands=None):
        self.data = self._loadData(filename)
        if commands:
            self.commands = commands
        else:
            self.commands = DefaultCommands()
            
    def _loadData(self, filename):
        events = []
        with open(filename, "r") as f:
            for line in f:
                event = json.loads(line)
                events.append(event)
        return events        
        
    def execute(self, command):
        tokens = self._parseCommand(command)
        if self._contains(tokens, ['count', 'events']):
            self.commands.printEventCount(self.data)
        elif self._contains(tokens, ['count', 'sessions']):
            self.commands.printSessionCount(self.data)
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
    filename = os.path.join(os.path.dirname(__file__), 'tests/testdata/data1.log')
    runtime = Runtime(filename)
    runtime.execute('Count sessions')