# -*- coding: utf-8 -*-
'''
Created on 24-08-2013

@author: Krzysztof Langner

Example commands:

print number of sessions
print session count
print last 20 events
'''
import json
import os.path
import nltk
import dateutil.parser
from datetime import date


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
    
    
class Tagger():
    ''' 
    Tagger codes:
      * NAME - name
      * DATE - date 
      * OBJ - object
      * CMD - command
    '''
    
    def tag(self, word):
        value = self._to_date(word)
        if value:
            return (value, 'DATE')
        return (word, 'NAME')
        
    def _to_date(self, word):
        try:
            return dateutil.parser.parse(word)
        except:
            if word == 'today':
                return date.today()
            return False    
        

class Runtime():
    
    def __init__(self, commands):
        self.commands = commands
            
    def execute(self, command):
        tokens = self._parseCommand(command)
        if self._contains(tokens, [('count', ''), ('event', '')]):
            self.commands.printEventCount()
        elif self._contains(tokens, [('count', ''), ('session', '')]):
            self.commands.printSessionCount()
        else:
            self.commands.notRecognized()
            
    def _parseCommand(self, command):
        tokens = nltk.word_tokenize(command.lower())
        porter = nltk.PorterStemmer()
        stems = [porter.stem(token) for token in tokens]
        tagger = Tagger()
        tagged_words = [tagger.tag(stem) for stem in stems]
        return tagged_words
            
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