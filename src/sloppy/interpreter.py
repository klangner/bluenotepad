# -*- coding: utf-8 -*-
'''
Created on 24-08-2013

@author: Krzysztof Langner

Example commands:

print number of sessions
print session count
print last 20 events
'''
import nltk
import os.path
import dateutil.parser
from datetime import date


class Parser():
    ''' 
    Tagger codes:
      * NAME - "name"
      * DATE - date 
      * KEYWORD - Keyword
      * NR = Not Recognized
    '''
    
    def __init__(self):
        self.keywords = dict()
        self.names = []
        self.porter = nltk.PorterStemmer()
        
    def add_keywords(self, names):
        normalized_names = [self.porter.stem(name.lower().strip()) for name in names]
        if len(normalized_names) > 0:
            self.keywords[normalized_names[0]] = normalized_names
        
    def parse(self, command):
        tokens = self._tokenize(command)
        stemmed_tokens = self._stem_tokens(tokens)
        tagged_tokens = self._tag_tokens(stemmed_tokens)
        return tagged_tokens
        
    def _tokenize(self, command):
        ''' Preserve names like "Page loaded" or 'Module edited'
        '''
        tokens = nltk.word_tokenize(command.lower())
        tags = []
        name = None
        for token in tokens:
            if token == '``':
                name = ''
            elif token == "''":
                tags.append((name, 'NAME'))
                name = None
            elif name != None:
                if len(name) > 0:
                    name += ' '
                name += token
            else:
                tags.append((token, ''))
        return tags
                
    
    def _stem_tokens(self, tokens):
        porter = nltk.PorterStemmer()
        stemmed_tokens = []
        for token in tokens:
            if token[1]:
                stemmed_tokens.append(token)
            else:
                stemmed_tokens.append((porter.stem(token[0]), ''))
        return stemmed_tokens
    
    def _tag_tokens(self, tokens):
        tagged_tokens = []
        for token in tokens:
            if token[1]:
                tagged_tokens.append(token)
            else:
                tagged_tokens.append(self._tag(token[0]))
        return tagged_tokens
    
    def _tag(self, word):
        value = self._get_keyword(word)
        if value:
            return (value, 'KEYWORD')
        value = self._get_date(word)
        if value:
            return (value, 'DATE')
        return (word, 'NR')
    
    def _get_keyword(self, name):
        for action, action_names in self.keywords.iteritems():
            if name in action_names:
                return action
        
    def _get_date(self, word):
        try:
            return dateutil.parser.parse(word)
        except:
            if word == 'today':
                return date.today()

    def _to_command(self, word):
        for command, synonims in self.commands.iteritems():
            if command == word or word in synonims:
                return command

class Runtime():
    
    def __init__(self):
        self.mappings = []
        self.parser = Parser()
        
    def add_mapping(self, features, fun):
        ''' Maps features to function which should ba called '''
        self.mappings.append((features, fun))
            
    def execute(self, command):
        features = self.parser.parse(command)
        for item in self.mappings:
            if self._contains(item[0], features):
                item[1](features)
            
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
#    runtime = Runtime(DefaultCommands(folder))
#    runtime.execute('Count sessions')