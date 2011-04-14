# pylint: disable-msg=W0401,W0614
from django.conf.urls.defaults import *

urlpatterns = patterns('serie.views',
    url(r'^(?P<serie_slug>[-\w]+)/$', 'get_serie', name='get_serie'),
    url(r'^(?P<serie_slug>[-\w]+)/season/(?P<season>\d+)/$', 'season_lookup', name='get_season'),
    url(r'^(?P<serie_slug>[-\w]+)/episode/S(?P<season>\d+)E(?P<episode>\d+)/$', 'get_episode', name='get_episode'),
    url(r'^(?P<serie_slug>[-\w]+)/episode/S(?P<season>\d+)E(?P<episode>\d+)/add/$', 'add_link', name='add_link'),
)
