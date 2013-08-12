'''
Created on 05-08-2013

@author: klangner
'''
from bluenotepad.storage.log import read_sessions
import os

DATA_ROOT = os.path.join(os.path.dirname(__file__), '../../data/')


def analyze_sessions(filename):
    sessions = read_sessions(filename)
    counter, counter2 = 0, 0
    for events in sessions.itervalues():
        if len(events) == 1:
            counter += 1
        elif len(events) == 2:
            counter2 += 1
    print( 'Single event sessions: %d' % counter)
    print( 'Double events sessions: %d' % counter2)
    print( 'All sessions: %d' % len(sessions))


if __name__ == '__main__':
    files = ['2013-08-06', '2013-08-07', '2013-08-08', '2013-08-09']
    for filename in files:
        print(filename)
        analyze_sessions(DATA_ROOT + filename + '.log')
        print
