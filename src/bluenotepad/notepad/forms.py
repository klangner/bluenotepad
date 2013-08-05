# -*- coding: utf-8 -*-
from django import forms


class ProjectForm(forms.Form):
    title = forms.CharField()
    url = forms.CharField(required=False)
    info = forms.CharField(required=False)


class NoteForm(forms.Form):
    noteID = forms.CharField()
    noteText = forms.CharField()


class StatDefinitionForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    rules = forms.CharField()
