# -*- coding: utf-8 -*-
from django import forms


class NotepadForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(required=False)
    report_model = forms.CharField(required=False)


class NoteForm(forms.Form):
    noteID = forms.CharField()
    noteText = forms.CharField()


class ReportForm(forms.Form):
    title = forms.CharField()
    code = forms.CharField()
    code = forms.CharField(required=False)