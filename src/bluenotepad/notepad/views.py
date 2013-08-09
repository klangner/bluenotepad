# -*- coding: utf-8 -*-
'''
Created on 2012-12-01

@author: Krzysztof Langner
'''
from bluenotepad.notepad.forms import NotepadForm, NoteForm
from bluenotepad.notepad.models import Notepad, DailyStats, StatDefinition
from bluenotepad.settings import FILE_STORAGE
from django.contrib.auth.decorators import login_required
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
import datetime
import os
from bluenotepad.storage.log import read_recent_events


@login_required
def index(request):
    notepads = Notepad.objects.filter(owner=request.user).order_by('-created_at')
    return render_to_response('notepad/index.html', 
                              {'notepads':notepads},
                              context_instance=RequestContext(request))


@login_required
def recent_sessions(request, notepad_id):
    notepad = get_object_or_404(Notepad, pk=notepad_id)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = FILE_STORAGE + notepad.uuid + "/" + today + ".log" 
    events = read_recent_events(filename)
    for event in events:
        event['time'] = datetime.datetime.strptime(event['time'], "%Y-%m-%dT%H:%M:%S")
    return render_to_response('notepad/recent_sessions.html', 
                              {'notepad': notepad,
                               'sessions': reversed(events),
                               'active_tab': 'recent'},
                              context_instance=RequestContext(request))


@login_required
def create_notepad(request):
    form = None
    if request.method == 'POST':
        form = NotepadForm(request.POST)
        if form.is_valid():
            notepad = Notepad()
            notepad.assignID()
            notepad.owner = request.user
            notepad.title = form.cleaned_data['title']
            notepad.description = form.cleaned_data['info']
            notepad.save()
            return HttpResponseRedirect('/notepad')
    return render_to_response('notepad/create_notepad.html', {'form':form}, 
                              context_instance=RequestContext(request))


@login_required
def stats(request, notepad_id):
    notepad = get_object_or_404(Notepad, pk=notepad_id)
    stats = DailyStats.objects.filter(notepad=notepad).order_by('-day')
    return render_to_response('notepad/daily_stats.html', 
                              {'notepad': notepad,
                               'stats': stats,
                               'active_tab': 'stats'},
                              context_instance=RequestContext(request))


@login_required
def sessions(request, notepad_id):
    notepad = get_object_or_404(Notepad, pk=notepad_id)
#    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
#    yesterday = today - timedelta(days=1)
    sessions = []
    bins = [0]*20
    for sessions in sessions:
        index = min(sessions.events/10, 19)
        bins[index] += 1
    return render_to_response('notepad/sessions.html', 
                              {'notepad': notepad,
                               'bins': bins,
                               'active_tab': 'session_stats'},
                              context_instance=RequestContext(request))


@login_required
def edit_note(request, notepad_id):
    if request.method == 'POST':
        notepad = get_object_or_404(Notepad, pk=notepad_id)
        form = NoteForm(request.POST)
        if form.is_valid() and notepad.owner == request.user:
            stats = get_object_or_404(DailyStats, pk=form.cleaned_data['noteID'])
            stats.notes = form.cleaned_data['noteText']
            stats.save()
    return HttpResponseRedirect('stats')


@login_required
def files(request, notepad_id):
    notepad = get_object_or_404(Notepad, pk=notepad_id)
    files = []
    try:
        for f in os.listdir(FILE_STORAGE + notepad.uuid):
            if f.endswith('.gz'):
                files.append(f)
    except OSError:
        pass
    return render_to_response('notepad/files.html', 
                              {'notepad': notepad,
                               'files': sorted(files, reverse=True),
                               'active_tab': 'files'},
                              context_instance=RequestContext(request))
    
    
@login_required
def download(request, notepad_id):
    notepad = get_object_or_404(Notepad, pk=notepad_id)
    filename = request.GET['file']
    filepath = FILE_STORAGE + notepad.uuid + "/" + filename
    f = open(filepath, "r")
    response = HttpResponse(FileWrapper(f), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s' % (filename)
    return response    


@login_required
def settings(request, notepad_id):
    notepad = get_object_or_404(Notepad, pk=notepad_id)
    stats = StatDefinition.objects.filter(notepad=notepad)
    return render_to_response('notepad/settings.html', 
                              {'notepad': notepad,
                               'stats': stats,
                               'active_tab': 'settings'},
                              context_instance=RequestContext(request))
