# -*- coding: utf-8 -*-
'''
Created on 24-08-2013

@author: Krzysztof Langner
'''
import sloppy.nlp as nlp
import unittest

class Test(unittest.TestCase):


    def testTokenizer1(self):
        sentence = 'Plot session histogram'
        tokens = nlp.tokenize(sentence)
        self.assertEqual(3, len(tokens))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTokenizer1']
    unittest.main()