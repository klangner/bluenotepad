from django.conf.urls.defaults import patterns


urlpatterns = patterns('bluenotepad.api.views',
    (r'^log$', 'log'),
)

