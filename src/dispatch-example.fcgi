#!/usr/bin/python
import sys, os

os.environ['DJANGO_SETTINGS_MODULE'] = "bluenotepad.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false") 