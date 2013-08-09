'''
Created on 05-08-2013

@author: klangner
'''
from collections import defaultdict
from bluenotepad.storage.log import read_sessions
import os

DATA_ROOT = os.path.join(os.path.dirname(__file__), '../../data/')


def count_events(sessions, events):
    all_events_counter, events_counter = 0, 0
    for records in sessions.itervalues():
        for record in records:
            all_events_counter += 1
            if record['event'] in events:
                events_counter += 1
    pct = events_counter*100/all_events_counter
    print("%s: %d (%d%%)" % (events[0], events_counter, pct))    
    return events_counter


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


def analyze_events(filename):
    sessions = read_sessions(filename)
#    long_sessions = {k:v for k,v in sessions.iteritems() if len(v) > 200}
    count_events(sessions, ['Insert module'])
    count_events(sessions, ['Module repositioned'])
    count_events(sessions, ['Remove module'])
    count_events(sessions, ['Change page height'])
    count_events(sessions, ['Duplicate page'])
    count_events(sessions, ['Show preview'])
    count_events(sessions, ['Paste module'])
    count_events(sessions, ['Save'])
    print 'All events: %d\n' % sum([len(v) for v in sessions.itervalues()])



def analyze_event_frequency(filename):
    sessions = read_sessions(filename)
    events = defaultdict(int)
    for records in sessions.itervalues():
        for record in records:
            name = record['event']
            events[name] += 1
    for name, counter in events.iteritems():
        if counter > 100:
            print name, ":\t", counter
    print '\n'

if __name__ == '__main__':
#    analyze_sessions(DATA_ROOT + '2013-08-06.log')
#    analyze_events(DATA_ROOT + '2013-08-07.log')
    analyze_event_frequency(DATA_ROOT + '2013-08-06.log')
    analyze_event_frequency(DATA_ROOT + '2013-08-07.log')
    analyze_event_frequency(DATA_ROOT + '2013-08-08.log')
