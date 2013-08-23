from django.conf.urls.defaults import patterns


urlpatterns = patterns('bluenotepad.notepad.views',
    (r'^$', 'index'),
    (r'^create$', 'create_notepad'),
    (r'^(?P<notepad_id>\d+)$', 'stats'),
    (r'^(?P<notepad_id>\d+)/recent$', 'recent_sessions'),
    (r'^(?P<notepad_id>\d+)/stats$', 'stats'),
    (r'^(?P<notepad_id>\d+)/report$', 'reports'),
    (r'^(?P<notepad_id>\d+)/download$', 'download'),
    (r'^(?P<notepad_id>\d+)/settings$', 'settings'),
    (r'^(?P<notepad_id>\d+)/edit_note$', 'edit_note'),
    (r'^(?P<notepad_id>\d+)/create_report$', 'create_report'),
    (r'^(?P<notepad_id>\d+)/edit_report/(?P<report_id>\d+)$', 'edit_report'),
    (r'^(?P<notepad_id>\d+)/execute_report/(?P<report_id>\d+)$', 'execute_report'),
)

