from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('liberweb.serie.views',
    url(r'^(?P<serie_slug>[-\w]+)/$', 'get_serie', name='get_serie'),
    (r'^(?P<serie_slug>[-\w]+)/episodes/$', 'get_episodes'),
    (r'^(?P<serie_slug>[-\w]+)/episodes/S(?P<season>\d+)E(?P<episode>\d+)/$', 'get_episode'),
)
