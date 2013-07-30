# -*- coding: utf-8 -*-
'''
Created on 24-03-2013

@author: Krzysztof Langner
'''
from django.shortcuts import render_to_response


def index(request):
    return render_to_response('public/index.html')
