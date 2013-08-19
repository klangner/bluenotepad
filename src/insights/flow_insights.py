# -*- coding: utf-8 -*-
'''
Created on 05-08-2013

@author: klangner
'''
from bluenotepad.storage.log import read_folder_sessions, read_sessions
from collections import defaultdict
import os


DATA_ROOT = os.path.join(os.path.dirname(__file__), '../../data/')


def event_before(sesions, event_name):
    events = defaultdict(int)
    for records in sessions.itervalues():
        last_record = None
        for record in records:
            if record['event'] == event_name:
                events[last_record['event']] += 1
            last_record = record 
    for name, counter in events.iteritems():
        print name, ":\t", counter


if __name__ == '__main__':
#    sessions = read_folder_sessions(DATA_ROOT)
    sessions = read_sessions(DATA_ROOT + '2013-08-14.log')
    event_before(sessions, 'Show preview')
