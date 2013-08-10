# -*- coding: utf-8 -*-
'''
Created on 07-08-2013

@author: Krzysztof Langner
'''
from collections import defaultdict
import json
import os.path

def read_sessions(filename):
    sessions = defaultdict(list)
    try:
        with open(filename, "r") as f:
            for line in f:
                event = json.loads(line)
                session_name = event['session']
                sessions[session_name].append(event)
            f.close()
    except IOError:
        pass
    return sessions


def read_recent_events(filename):
    events = []
    try:
        with open(filename, "r") as f:
            size = os.path.getsize(filename)
            if size > 8000:
                f.seek(size-8000)
                f.readline()
            for line in f.readlines():
                events.append(json.loads(line))
    except IOError:
        pass
    return events