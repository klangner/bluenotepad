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
    counter = 0
    for session,events in sessions.iteritems():
        if len(events) == 1:
            counter += 1
            print( "%s: %s" % (session, events[0]['event']))
    print( 'Found %d 1 event sessions out of all %d sessions' % (counter, len(sessions)))


if __name__ == '__main__':
    filename = DATA_ROOT + '2013-08-06.log' 
    analyze_sessions(filename)
