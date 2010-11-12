from django.conf.urls.defaults import patterns

urlpatterns = patterns('liberweb.serie.views',
    (r'^(?P<serie_slug>[-\w]+)/$', 'get_serie'),
    (r'^(?P<serie_slug>[-\w]+)/episodes/$', 'get_episodes'),
    (r'^(?P<serie_slug>[-\w]+)/episodes/S(?P<season>\d+)E(?P<episode>\d+)/$', 'get_episode'),
)
