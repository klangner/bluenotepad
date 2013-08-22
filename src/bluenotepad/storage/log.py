# -*- coding: utf-8 -*-
'''
Created on 07-08-2013

@author: Krzysztof Langner
'''
from collections import defaultdict
import json
import os.path

PREVIEW_LOG_SIZE = 30000

def read_sessions(filename):
    sessions = defaultdict(list)
    try:
        with open(filename, "r") as f:
            for line in f:
                event = json.loads(line)
                session_name = event['session']
                sessions[session_name].append(event)
    except IOError:
        pass
    return sessions


def read_recent_sessions(filename):
    sessions = defaultdict(list)
    try:
        with open(filename, "r") as f:
            size = os.path.getsize(filename)
            if size > PREVIEW_LOG_SIZE:
                f.seek(size-PREVIEW_LOG_SIZE)
                f.readline()
            for line in f.readlines():
                event = json.loads(line)
                session_name = event['session']
                sessions[session_name].append(event)
    except IOError:
        pass
    sessions.default_factory = None
    return sessions


def read_folder_sessions(folder):
    sessions = defaultdict(list)
    for filename in os.listdir(folder):
        with open(folder+filename, "r") as f:
            for line in f:
                event = json.loads(line)
                session_name = event['session']
                sessions[session_name].append(event)
    return sessions