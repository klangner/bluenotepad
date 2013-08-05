# -*- coding: utf-8 -*-
'''
Created on 2013-07-31

@author: Krzysztof Langner
'''

from django.contrib.auth.models import User
from django.db import models

class Notepad(models.Model):
    owner = models.ForeignKey(User)
    uuid = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'%s: %s' % (self.owner, self.title)


class StatDefinition(models.Model):
    notepad = models.ForeignKey(Notepad)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    rules = models.TextField()
    
    
class DailyStats(models.Model):
    notepad = models.ForeignKey(Notepad)
    day = models.DateField()
    all_events = models.IntegerField(default=0)
    sessions = models.IntegerField(default=0)
    notes = models.TextField()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'%s %s' % (self.notepad, self.day)

    
class StatData(models.Model):
    daily_stats = models.ForeignKey(DailyStats)
    title = models.CharField(max_length=200)
    rules = models.TextField()
    value = models.IntegerField(default=0)
    
    
    