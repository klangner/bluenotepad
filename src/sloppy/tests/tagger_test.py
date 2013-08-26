# -*- coding: utf-8 -*-
'''
Created on 24-08-2013

@author: Krzysztof Langner
'''
from sloppy.interpreter import Tagger
import dateutil.parser
from datetime import date
import unittest

class Test(unittest.TestCase):

    def testNoTag(self):
        tagger = Tagger()
        tag = tagger.tag('ala')
        self.assertEqual(('ala','NAME'), tag)

    def testDate1(self):
        tagger = Tagger()
        tag = tagger.tag('2013-01-20')
        expected = (dateutil.parser.parse('2013-01-20'), 'DATE')
        self.assertEqual(expected, tag)

    def testToday(self):
        tagger = Tagger()
        tag = tagger.tag('today')
        expected = (date.today(), 'DATE')
        self.assertEqual(expected, tag)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTokenizer1']
    unittest.main()