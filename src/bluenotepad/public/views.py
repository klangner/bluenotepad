# -*- coding: utf-8 -*-
'''
Created on 24-03-2013

@author: Krzysztof Langner
'''
from bluenotepad.settings import FILE_STORAGE
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def index(request):
    return render_to_response('public/index.html', context_instance=RequestContext(request))


def dataset(request, filename):
    filepath = FILE_STORAGE + "_public/datasets/" + filename
    try:
        f = open(filepath, "r")
        response = HttpResponse(FileWrapper(f), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=%s' % (filename)
        return response    
    except IOError:
        return HttpResponseRedirect('/')
    