from django.conf.urls.defaults import *

urlpatterns = patterns('api.views',
    url(r'^series$', 'series_list'),
    url(r'^serie/(?P<id_serie>\d+)$', 'serie_detail'),
    url(r'^serie/(?P<id_serie>\d+)/S(?P<season>\d+)$', 'season_detail'),
    url(r'^serie/(?P<id_serie>\d+)/S(?P<season>\d+)E(?P<episode>\d+)$', 'episode_detail'),
)
