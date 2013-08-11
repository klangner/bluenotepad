'''
Created on 01-08-2013

@author: klangner
'''
from collections import defaultdict
from bluenotepad.notepad.models import Notepad, DailyStats
from bluenotepad.notepad.parser import parseReportModel
from bluenotepad.settings import FILE_STORAGE
from bluenotepad.storage.log import read_sessions
from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
import gzip
import os


class Command(BaseCommand):
    args = '<...>'
    help = 'Aggregate statistics'

    def handle(self, *args, **options):
        notepads = Notepad.objects.all();
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)
        file_date = yesterday.strftime("%Y-%m-%d")
        counter = 0 
        for notepad in notepads:
            filename = FILE_STORAGE + notepad.uuid + "/" + file_date + ".log"
            sessions = read_sessions(filename)
            stats = DailyStats(notepad=notepad)
            stats.day = yesterday.date()
            stats.session_count = len(sessions)
            stats.event_count = sum([len(events) for events in sessions.itervalues()])
            stats.report_data = self.createReport(sessions, notepad)
            stats.save()
            counter += 1
            self.compressLog(filename)
        self.stdout.write('Aggregate command processed %d notepads\n' % (counter))
        
    def createReport(self, sessions, notepad):
        report = ''
        event_count = sum([len(events) for events in sessions.itervalues()])
        variables = parseReportModel(notepad.report_model)
        data = defaultdict(int)
        for records in sessions.itervalues():
            for record in records:
                for var_name, var_events in variables.iteritems():
                    if record['event'] in var_events:
                        data[var_name] += 1
        for key, value in data.iteritems():
            report += ('%s: %d (%d%%)\n' % (key, value, (value*100)/event_count))
        return report
        
    def compressLog(self, filename):
        if os.path.exists(filename):
            f_in = open(filename, 'rb')
            f_out = gzip.open(filename + '.gz', 'wb')
            f_out.writelines(f_in)
            f_out.close()
            f_in.close()
