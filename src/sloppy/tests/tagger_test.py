# -*- coding: utf-8 -*-
'''
Created on 24-08-2013

@author: Krzysztof Langner
'''
from sloppy.interpreter import Tagger
import unittest

class Test(unittest.TestCase):

    def testNoTag(self):
        tagger = Tagger()
        tag = tagger.tag('ala')
        self.assertEqual(('ala','NR'), tag)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTokenizer1']
    unittest.main()