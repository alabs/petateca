from django.conf.urls.defaults import *

urlpatterns = patterns('tracking.views',

    url(r'^show/$', 'show_tracking', name='show_tracking'),
    url(r'^set/$', 'set_tracking', name='set_tracking'),

)
