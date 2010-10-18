from django.conf.urls.defaults import *

urlpatterns = patterns('liberweb.serie.views',
        (r'^$', 'index'),
        (r'^by_date', 'by_date'),
        (r'^by_popularity', 'by_popularity'),
        (r'^by_review', 'by_review'),
        (r'^(?P<serie_slug>[a-z0-9-]+)/$', 'get_serie'),
        (r'^(?P<serie_slug>[a-z0-9-]+)/episodes/$', 'get_episodes'),
        (r'^(?P<serie_slug>[a-z0-9-]+)/episodes/(?P<episode_slug>[a-z0-9-]+)/$', 'get_episode'),
)

