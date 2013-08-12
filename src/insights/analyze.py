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


# Sprawdzić czy są pomyłki przy wstawianiu modułów:
#  - Wstawienie modułu -> usunięcie -> Wstawienie noweg
def analyze_events(filename):
    sessions = read_sessions(filename)
#    long_sessions = {k:v for k,v in sessions.iteritems() if len(v) > 200}
    count_events(sessions, ['Save'])
    count_events(sessions, ['Show preview'])
    count_events(sessions, ['Module repositioned'])
    count_events(sessions, ['Change page height'])
    count_events(sessions, ['Paste module'])
    count_events(sessions, ['Module removed'])
    count_events(sessions, ['Remove page'])
    print 'All events: %d' % sum([len(v) for v in sessions.itervalues()])



def analyze_event_frequency(filename):
    sessions = read_sessions(filename)
    events = defaultdict(int)
    for records in sessions.itervalues():
        for record in records:
            name = record['event']
            events[name] += 1
    for name, counter in events.iteritems():
        print name, ":\t", counter


def analyze(filenames, fun):
    for filename in filenames:
        print filename
        fun(DATA_ROOT + filename + '.log')
        print '\n'


if __name__ == '__main__':
    files = ['2013-08-06', '2013-08-07', '2013-08-08', '2013-08-09']
    analyze(files, analyze_events)
