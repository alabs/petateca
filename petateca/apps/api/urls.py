from django.conf.urls.defaults import *

urlpatterns = patterns('api.views',
    url(r'^/series$', 'series_list'),
    url(r'^/serie/(?P<id_serie>\d+)$', 'serie_detail', name='API_serie_detail'),
    url(r'^/serie/(?P<id_serie>\d+)/S(?P<season>\d+)$', 'season_detail', name='API_season_detail'),
    url(r'^/serie/(?P<id_serie>\d+)/S(?P<season>\d+)E(?P<episode>\d+)$', 'episode_detail', name='API_episode_detail'),
)

urlpatterns += patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template',
        {'template': 'api.html'},
        name="api"
       ),
)
