# -*- coding: utf-8 -*-
'''
Created on 2012-12-01

@author: Krzysztof Langner
'''
from bluenotepad.notepad.forms import NotepadForm
from bluenotepad.notepad.models import Notepad, DailyStats, StatDefinition
from bluenotepad.settings import FILE_STORAGE
from django.contrib.auth.decorators import login_required
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
import datetime
import json
import os


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
    sessions = []
    try:
        log_file = open(filename, 'r')
        for line in log_file.readlines()[:50]:
            data = json.loads(line)
            if data['time'].find('T') > 0: 
                data['time'] = datetime.datetime.strptime(data['time'], "%Y-%m-%dT%H:%M:%S")
            else:
                data['time'] = datetime.datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
            sessions.append(data)
    except IOError:
        pass
    return render_to_response('notepad/recent_sessions.html', 
                              {'notepad': notepad,
                               'sessions': sessions,
                               'active_tab': 1},
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
                               'active_tab': 0},
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
                               'active_tab': 2},
                              context_instance=RequestContext(request))


#@login_required
#def edit_note(request, project_id):
#    if request.method == 'POST':
#        project = Project.get_by_id(int(project_id))
#        form = NoteForm(request.POST)
#        if form.is_valid():
#            stats = DailyStats.get_by_id(int(form.cleaned_data['noteID']), parent=project)
#            if stats:
#                stats.notes = form.cleaned_data['noteText']
#                stats.put()
#            else:
#                return HttpResponse('Wrong id: ' + form.cleaned_data['noteID'])
#    return HttpResponseRedirect('stats')


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
                               'files': files,
                               'active_tab': 3},
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
                               'active_tab': 10},
                              context_instance=RequestContext(request))
