# -*- coding: utf-8 -*-
'''
Created on 24-08-2013

@author: Krzysztof Langner
'''
from datascript.tokens import Tokenizer
import unittest

class TokenizerTest(unittest.TestCase):

    def testToken1(self):
        tokenizer = Tokenizer()
        token = tokenizer.next_token('count events')
        self.assertEqual('count', token[0][0])
        self.assertEqual(Tokenizer.IDENTIFIER_TYPE, token[0][1])
        self.assertEqual(' events', token[1])

    def testToken2(self):
        tokenizer = Tokenizer()
        token1 = tokenizer.next_token('count events')
        token2 = tokenizer.next_token(token1[1])
        self.assertEqual('events', token2[0][0])
        self.assertEqual(Tokenizer.IDENTIFIER_TYPE, token2[0][1])
        self.assertEqual('', token2[1])

    def testUnderscore(self):
        tokenizer = Tokenizer()
        token = tokenizer.next_token('count_events ')
        self.assertEqual('count_events', token[0][0])
        self.assertEqual(Tokenizer.IDENTIFIER_TYPE, token[0][1])
        self.assertEqual(' ', token[1])

    def testVal(self):
        tokenizer = Tokenizer()
        token = tokenizer.next_token('val events')
        self.assertEqual('val', token[0][0])
        self.assertEqual(Tokenizer.KEYWORD_TYPE, token[0][1])
        self.assertEqual(' events', token[1])
        
    def testEmptyCommand(self):
        tokenizer = Tokenizer()
        # Token 1
        token1 = tokenizer.next_token('text2.hide()')
        self.assertEqual('text2', token1[0][0])
        self.assertEqual(Tokenizer.IDENTIFIER_TYPE, token1[0][1])
        # Token 2
        token2 = tokenizer.next_token(token1[1])
        self.assertEqual('.', token2[0][0])
        self.assertEqual(Tokenizer.DELIMETER_TYPE, token2[0][1])
        # Token 3
        token3 = tokenizer.next_token(token2[1])
        self.assertEqual('hide', token3[0][0])
        self.assertEqual(Tokenizer.IDENTIFIER_TYPE, token3[0][1])
        # Token 4
        token4 = tokenizer.next_token(token3[1])
        self.assertEqual('(', token4[0][0])
        self.assertEqual(Tokenizer.DELIMETER_TYPE, token4[0][1])
        # Token 5
        token5 = tokenizer.next_token(token4[1])
        self.assertEqual(')', token5[0][0])
        self.assertEqual(Tokenizer.DELIMETER_TYPE, token5[0][1])
        
    def testSingleIntParam(self):
        tokenizer = Tokenizer()
        # Token 1
        token1 = tokenizer.next_token('(3)')
        self.assertEqual('(', token1[0][0])
        self.assertEqual(Tokenizer.DELIMETER_TYPE, token1[0][1])
        # Token 2
        token2 = tokenizer.next_token(token1[1])
        self.assertEqual('3', token2[0][0])
        self.assertEqual(Tokenizer.INTEGER_TYPE, token2[0][1])
        self.assertEqual(')', token2[1])
        
    def testFloats(self):
        tokenizer = Tokenizer()
        # Token 1
        token1 = tokenizer.next_token('34.5 .23 ')
        self.assertEqual('34.5', token1[0][0])
        self.assertEqual(Tokenizer.FLOAT_TYPE, token1[0][1])
        # Token 2
        token2 = tokenizer.next_token(token1[1])
        self.assertEqual('.23', token2[0][0])
        self.assertEqual(Tokenizer.FLOAT_TYPE, token2[0][1])
        self.assertEqual(' ', token2[1])
        
    def testComma(self):
        tokenizer = Tokenizer()
        # Token 1
        token1 = tokenizer.next_token('34.5, 23')
        self.assertEqual('34.5', token1[0][0])
        self.assertEqual(Tokenizer.FLOAT_TYPE, token1[0][1])
        # Token 2
        token2 = tokenizer.next_token(token1[1])
        self.assertEqual(',', token2[0][0])
        self.assertEqual(Tokenizer.DELIMETER_TYPE, token2[0][1])
        self.assertEqual(' 23', token2[1])
        
    def testLiteral(self):
        tokenizer = Tokenizer()
        # Token 1
        token = tokenizer.next_token('"Deep space" ')
        self.assertEqual('Deep space', token[0][0])
        self.assertEqual(Tokenizer.LITERAL_TYPE, token[0][1])
        self.assertEqual(' ', token[1])
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTokenizer1']
    unittest.main()