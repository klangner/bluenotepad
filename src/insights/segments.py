'''
Created on 05-08-2013

@author: klangner
'''
from bluenotepad.storage.log import read_sessions
import os
import pylab as plt

DATA_ROOT = os.path.join(os.path.dirname(__file__), '../../data/')


def analyze_sessions(filename, threshold):
    sessions = read_sessions(filename)
    counter = 0
    for events in sessions.itervalues():
        if len(events) < threshold:
            counter += 1
    print( 'Below threshold: %d' % counter)
    print( 'All sessions: %d' % len(sessions))


def session_histogram(filename):
    sessions = read_sessions(filename)
    data = [min(len(events),200) for events in sessions.itervalues()]
#    data = [len(events) for events in sessions.itervalues()]
    plt.ylabel('Number of sessions')
    plt.xlabel('Number of actions')
    plt.title('Histogram of session activity')
    plt.hist(data, bins=20, range=[0, 200])
#    plt.hist(data, log=True)
    plt.show()

if __name__ == '__main__':
#    analyze_sessions(DATA_ROOT + '2013-08-14.log', 2)
    session_histogram(DATA_ROOT + '2013-08-14.log')
