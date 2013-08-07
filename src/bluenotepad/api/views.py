# -*- coding: utf-8 -*-
'''
Created on 2012-12-01

@author: Krzysztof Langner
'''
from bluenotepad.settings import FILE_STORAGE
from django.http import HttpResponse
import datetime
import json
import os

def log(request):
    notepad_id = request.GET['notepad']
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = FILE_STORAGE + notepad_id + "/" + today + ".log" 
    try:
        log_file = open(filename, 'a+')
    except IOError:
        os.makedirs(FILE_STORAGE + notepad_id)
        log_file = open(filename, 'a+')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    data = {'time':timestamp}
    for key in request.GET:
        data[key] = request.GET[key] 
    log_file.write(json.dumps(data) + "\n")
    log_file.close()
    return HttpResponse('')
