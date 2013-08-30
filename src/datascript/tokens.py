# -*- coding: utf-8 -*-
'''
Created on 30-08-2013

@author: Krzysztof Langner
'''
import re

class Tokenizer:

    # Token types    
    INTEGER_TYPE  = 1
    FLOAT_TYPE = 2
    DELIMETER_TYPE = 3
    IDENTIFIER_TYPE = 4
    KEYWORD_TYPE = 5
    LITERAL_TYPE = 6
    ERROR_TYPE  = -1
          
    _SPACES_PATTERN = re.compile('^(\s+)(?P<rest>.*)')
    _IDENTIFIER_PATTERN = re.compile('^(?P<symbol>[a-zA-Z_]\w+)(?P<rest>.*)')
    _FLOAT_PATTERN = re.compile('^(?P<symbol>\d*\.\d+)(?P<rest>.*)')
    _INTEGER_PATTERN = re.compile('^(?P<symbol>\d+)(?P<rest>.*)')
    _DELIMETER = ',.()='
    _KEYWORDS = set('val'.split(' '))
    
    
    def next_token(self, text):
        if not text:
            return None
        match = self._IDENTIFIER_PATTERN.search(text)
        if match:
            symbol = match.group('symbol')
            if symbol in self._KEYWORDS:
                return ((symbol, self.KEYWORD_TYPE), match.group('rest'))
            else:
                return ((symbol, self.IDENTIFIER_TYPE), match.group('rest')) 
        match = self._SPACES_PATTERN.search(text)
        if match:
            return self.next_token(match.group('rest'))
        match = self._FLOAT_PATTERN.search(text)
        if match:
            return ((match.group('symbol'), self.FLOAT_TYPE), match.group('rest')) 
        match = self._INTEGER_PATTERN.search(text)
        if match:
            return ((match.group('symbol'), self.INTEGER_TYPE), match.group('rest')) 
        if text[0] in self._DELIMETER:
            return ((text[0], self.DELIMETER_TYPE), text[1:])
    
    
if __name__ == '__main__':
    tokenizer = Tokenizer()
    token = tokenizer.next_token("count events")
    print( token )