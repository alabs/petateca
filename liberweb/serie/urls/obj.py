from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('liberweb.serie.views',
    url(r'^(?P<serie_slug>[-\w]+)/$', 'get_serie', name='get_serie'),
    url(r'^(?P<serie_slug>[-\w]+)/season/(?P<season>\d+)/$', 'get_season', name='get_season'),
    url(r'^(?P<serie_slug>[-\w]+)/episode/S(?P<season>\d+)E(?P<episode>\d+)/$', 'get_episode', name='get_episode'),
)
