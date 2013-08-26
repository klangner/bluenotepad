# -*- coding: utf-8 -*-
'''
Created on 05-08-2013

@author: klangner
'''
from collections import defaultdict
from bluenotepad.storage.log import read_sessions
import os
import pylab as plt


DATA_ROOT = os.path.join(os.path.dirname(__file__), '../../data/')


def count_events(sessions, events):
    all_events_counter, events_counter = 0.0, 0.0
    for records in sessions.itervalues():
        for record in records:
            all_events_counter += 1
            if record['event'] in events:
                events_counter += 1
    if all_events_counter > 0:
        events_per_session = events_counter/len(sessions)
        pct = events_counter*100/all_events_counter
        print("%s: %d (%.2f%%) %.2f" % (events[0], events_counter, pct, events_per_session))    
    return events_counter, all_events_counter


def analyze_events(filename):
    sessions = read_sessions(filename)
#    sessions = {k:v for k,v in sessions.iteritems() if len(v) > 10}
#    count_events(sessions, ['Save'])
    count_events(sessions, ['Page page'])
    count_events(sessions, ['Insert page'])
#    count_events(sessions, ['Show preview'])
#    count_events(sessions, ['Module repositioned'])
#    count_events(sessions, ['Change page height'])
#    count_events(sessions, ['Module edited'])
#    count_events(sessions, ['Module removed'])
#    count_events(sessions, ['Remove page'])
    print 'Events: %d Sessions: %d' % (sum([len(v) for v in sessions.itervalues()]), len(sessions))



def analyze_event_frequency(filename):
    sessions = read_sessions(filename)
    events = defaultdict(int)
    for records in sessions.itervalues():
        for record in records:
            name = record['event']
            events[name] += 1
    print len(events)
    for name, counter in events.iteritems():
        print name, ":\t", counter


def analyze(filenames, fun):
    for filename in filenames:
        print filename
        fun(DATA_ROOT + filename + '.log')
        print '\n'


def analyze_folder(path, fun):
    for filename in os.listdir(path):
        print filename
        fun(path + filename)
        print '\n'
        
        
def calculate_waste(filename):
    sessions = read_sessions(filename)
    waste = ['Preferences', 'Export page', 'Page down', 'Start', 
             'Bring to front', 'Duplicate page', 'Save', 'Copy module', 
             'Page up', 'Module repositioned', 'Paste module', 'Show preview', 
             'Module removed', 'Change page height', 'Import page', 
             'Remove module', 'Remove page', 'Send back', 'Page loaded']
    return count_events(sessions, waste)


def plot_waste(folder):
    waste = []
    for filename in os.listdir(folder):
        print filename
        waste_events, all_events = calculate_waste(folder+filename) 
        waste.append(waste_events*100.0/all_events)
    plt.ylabel('Waste percentage')
    plt.xlabel('Day')
    plt.title('Waste percentage per day')
    plt.plot(waste)
    plt.ylim([0,100])
    plt.show()


if __name__ == '__main__':
#    sessions = read_sessions(DATA_ROOT + '2013-08-20.log')
#    count_events(sessions, ['Page loaded'])
#    calculate_waste(DATA_ROOT + '2013-08-20.log')
    analyze_folder(DATA_ROOT, analyze_event_frequency)
#    plot_waste(DATA_ROOT)
