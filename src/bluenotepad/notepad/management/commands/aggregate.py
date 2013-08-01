'''
Created on 01-08-2013

@author: klangner
'''
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = '<...>'
    help = 'Aggregate statistics'

    def handle(self, *args, **options):
        self.stdout.write('Command executed\n')
