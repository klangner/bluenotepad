from django.conf.urls.defaults import patterns


urlpatterns = patterns('bluenotepad.public.views',
    (r'^dataset/(?P<filename>.+)$', 'dataset'),
)

