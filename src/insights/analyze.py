'''
Created on 05-08-2013

@author: klangner
'''
from bluenotepad.storage.log import read_sessions
import json
import os

DATA_ROOT = os.path.join(os.path.dirname(__file__), '../../data/')


def count_events(filename, events):
    all_events_counter = 0
    events_counter = 0
    with open(filename, "r") as f:
        for line in f:
            event = json.loads(line)
            all_events_counter += 1
            if event['event'] in events:
                events_counter += 1
    pct = events_counter*100/all_events_counter
    print("Found %d (%d%%) out of %d events" % (events_counter, pct, all_events_counter))    


def analyze_sessions(filename):
    sessions = read_sessions(filename)
    counter, counter2 = 0, 0
    for _session,events in sessions.iteritems():
        if len(events) == 1:
            counter += 1
        elif len(events) == 2:
            counter2 += 1
    print( 'Single event sessions: %d' % counter)
    print( 'Double events sessions: %d' % counter2)
    print( 'All sessions: %d' % len(sessions))


if __name__ == '__main__':
    filename = DATA_ROOT + '2013-08-06.log'
    analyze_sessions(filename)
