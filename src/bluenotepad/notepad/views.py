# -*- coding: utf-8 -*-
'''
Created on 2012-12-01

@author: Krzysztof Langner
'''
from bluenotepad.notepad.forms import NotepadForm, NoteForm, ReportForm
from bluenotepad.notepad.models import Notepad, DailyStats, Report
from bluenotepad.settings import FILE_STORAGE
from bluenotepad.storage.log import read_recent_sessions
from django.contrib.auth.decorators import login_required
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
import datetime


@login_required
def index(request):
    notepads = Notepad.objects.filter(owner=request.user).order_by('title')
    return render_to_response('notepad/index.html', 
                              {'notepads':notepads},
                              context_instance=RequestContext(request))


@login_required
def recent_sessions(request, notepad_id):
    notepad = get_object_or_404(Notepad, pk=notepad_id)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = FILE_STORAGE + notepad.uuid + "/" + today + ".log" 
    sessions = read_recent_sessions(filename)
    for events in sessions.itervalues():
        for event in events:
            event['time'] = datetime.datetime.strptime(event['time'], "%Y-%m-%dT%H:%M:%S")
    return render_to_response('notepad/recent_sessions.html', 
                              {'notepad': notepad,
                               'sessions': sessions,
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
            notepad.description = form.cleaned_data['description']
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
    form = None
    if request.method == 'POST':
        form = NotepadForm(request.POST)
        if form.is_valid():
            notepad.title = form.cleaned_data['title']
            notepad.description = form.cleaned_data['description']
            notepad.report_model = form.cleaned_data['report_model']
            notepad.save()
    return render_to_response('notepad/settings.html', 
                              {'notepad': notepad,
                               'form': form,
                               'active_tab': 'settings'},
                              context_instance=RequestContext(request))


@login_required
def reports(request, notepad_id):
    notepad = get_object_or_404(Notepad, pk=notepad_id)
    reports = Report.objects.filter(notepad=notepad).order_by('-modified_at')
    return render_to_response('notepad/reports.html', 
                              {'notepad': notepad,
                               'reports': reports,
                               'active_tab': 'reports'},
                              context_instance=RequestContext(request))


@login_required
def create_report(request, notepad_id):
    notepad = get_object_or_404(Notepad, pk=notepad_id)
    form = None
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = Report(notepad=notepad)
            report.title = form.cleaned_data['title']
            report.code = form.cleaned_data['code']
            report.save()
            return HttpResponseRedirect('report')
    return render_to_response('notepad/create_report.html', 
                              {'form':form,
                               'notepad': notepad,
                               'active_tab': 'reports'}, 
                              context_instance=RequestContext(request))


@login_required
def edit_report(request, notepad_id, report_id):
    notepad = get_object_or_404(Notepad, pk=notepad_id)
    report = get_object_or_404(Report, pk=report_id)
    form = None
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report.title = form.cleaned_data['title']
            report.code = form.cleaned_data['code']
            report.save()
            return HttpResponseRedirect('/notepad/%s/report' % notepad_id)
    return render_to_response('notepad/edit_report.html', 
                              {'form':form,
                               'notepad': notepad,
                               'report':report,
                               'active_tab': 'reports'}, 
                              context_instance=RequestContext(request))


@login_required
def execute_report(request, notepad_id, report_id):
    notepad = get_object_or_404(Notepad, pk=notepad_id)
    report = get_object_or_404(Report, pk=report_id)
    return render_to_response('notepad/execute_report.html', 
                              {'notepad': notepad,
                               'report':report,
                               'active_tab': 'reports'}, 
                              context_instance=RequestContext(request))
