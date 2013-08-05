'''
Created on 05-08-2013

@author: klangner
'''
import json
import os
from collections import defaultdict

DATA_ROOT = os.path.join(os.path.dirname(__file__), '../../data/')


def read_sessions(filename):
    sessions = defaultdict(list)
    with open(filename, "r") as f:
        for line in f:
            event = json.loads(line)
            session_name = event['session']
            sessions[session_name].append(event)
    print(sessions)
    


def count_events(filename, events):
    all_events_counter = 0
    events_counter = 0
    with open(filename, "r") as f:
        for line in f:
            event = json.loads(line)
            all_events_counter += 1
            if event['event'] in events:
                events_counter += 1
    return (events_counter, all_events_counter)
    


if __name__ == '__main__':
    filename = DATA_ROOT + '2013-08-01.log' 
    (events, all_eventes) = count_events( filename, ['json'] )
    print("Found %d (%d%%) out of %d events" % (events, events*100/all_eventes, all_eventes))