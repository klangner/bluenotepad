# -*- coding: utf-8 -*-
'''
Created on 2012-12-01

@author: Krzysztof Langner
'''
from bluenotepad.settings import FILE_STORAGE
from django.http import HttpResponse
import datetime
import os

def log(request):
    notepad_id = request.GET['notepad']
    session_id = request.GET['session']
    event = request.GET['event']
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = FILE_STORAGE + notepad_id + "/" + today + ".log" 
    try:
        log_file = open(filename, 'a+')
    except IOError:
        os.makedirs(FILE_STORAGE + notepad_id)
        log_file = open(filename, 'a+')
    log_file.write("%s, %s, %s\n" %(session_id, timestamp, event))
    log_file.close()
    return HttpResponse('')
