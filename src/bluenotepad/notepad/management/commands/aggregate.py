'''
Created on 01-08-2013

@author: klangner
'''
from bluenotepad.notepad.models import Notepad
from bluenotepad.settings import FILE_STORAGE
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
        filename = yesterday.strftime("%Y-%m-%d") + ".log"
        counter = 0 
        for notepad in notepads:
            filepath = FILE_STORAGE + notepad.uuid + "/" + filename
            if os.path.exists(filepath):
                self.aggregate(filepath)
                self.compressLog(filepath)
                counter += 1
        self.stdout.write('Aggregate command processed %d files\n' % (counter))
        
    def aggregate(self, filename):
        f = open(filename, "r")
        f.close()
        
    def compressLog(self, filename):
        f_in = open(filename, 'rb')
        f_out = gzip.open(filename + '.gz', 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
