from django.conf.urls.defaults import patterns


urlpatterns = patterns('bluenotepad.notepad.views',
    (r'^$', 'index'),
#    (r'^create$', 'create_notepad'),
    (r'^(?P<notepad_id>\d+)$', 'notepad'),
    (r'^(?P<notepad_id>\d+)/stats$', 'stats'),
    (r'^(?P<notepad_id>\d+)/sessions$', 'sessions'),
    (r'^(?P<notepad_id>\d+)/files$', 'files'),
#    (r'^(?P<notepad_id>\d+)/edit_note$', 'edit_note'),
)

