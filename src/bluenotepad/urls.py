from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template
import os

admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('registration.backends.simple.urls')),                        
    url(r'^$', 'bluenotepad.public.views.index'),
    (r'^notepad/', include('bluenotepad.notepad.urls')),

    (r'^robots\.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'}),    
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'templates/media/')}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
