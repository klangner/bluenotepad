'''
Created on 01-08-2013

@author: klangner
'''
from bluenotepad.notepad.models import Notepad, DailyStats
from bluenotepad.settings import FILE_STORAGE
from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
from bluenotepad.storage.log import read_sessions
import gzip
import os


class Command(BaseCommand):
    args = '<...>'
    help = 'Aggregate statistics'

    def handle(self, *args, **options):
        notepads = Notepad.objects.all();
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)
        filename = yesterday.strftime("%Y-%m-%d") + ".log"
        counter = 0 
        for notepad in notepads:
            filepath = FILE_STORAGE + notepad.uuid + "/" + filename
            (sessions, events) = self.processLog(filepath)
            stats = DailyStats(notepad=notepad)
            stats.day = yesterday.date()
            stats.session_count = sessions
            stats.event_count = events
            stats.save()
            counter += 1
        self.stdout.write('Aggregate command processed %d notepads\n' % (counter))
        
    def processLog(self, filename):
        session_count = 0
        event_count = 0
        if os.path.exists(filename):
            sessions = read_sessions(filename)
            self.compressLog(filename)
            session_count = len(sessions)
            event_count = sum([len(events) for events in sessions.itervalues()])
        return session_count, event_count
        
    def compressLog(self, filename):
        f_in = open(filename, 'rb')
        f_out = gzip.open(filename + '.gz', 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
