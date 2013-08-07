# -*- coding: utf-8 -*-
'''
Created on 07-08-2013

@author: Krzysztof Langner
'''
import json
from collections import defaultdict

def read_sessions(filename):
    sessions = defaultdict(list)
    with open(filename, "r") as f:
        for line in f:
            event = json.loads(line)
            session_name = event['session']
            sessions[session_name].append(event)
        f.close()
    return sessions
