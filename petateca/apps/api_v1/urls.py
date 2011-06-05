from django.conf.urls.defaults import *

from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource

from api_v1 import handlers as h

auth = HttpBasicAuthentication(realm="Liberateca v1 API - Autenticacion")
ad = { 'authentication': auth }

serielist_resource = Resource(handler=h.SerieListHandler, **ad)
serie_resource = Resource(handler=h.SerieHandler, **ad)
seasonlist_resource = Resource(handler=h.SeasonListHandler, **ad)
season_resource = Resource(handler=h.SeasonHandler, **ad)
episode_resource = Resource(handler=h.EpisodeHandler, **ad)

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'api_v1.html'}),
    url(r'^series/$', serielist_resource, name='API_v1_serie_list'),
    url(r'^series/(?P<serie_id>\d+)/$', serie_resource, name='API_v1_serie_detail'),
    url(r'^series/(?P<serie_id>\d+)/seasons/$', seasonlist_resource, name='API_v1_season_list'),
    url(r'^series/(?P<serie_id>\d+)/(?P<season>\d+)/$', season_resource, name='API_v1_season_detail'),
    url(r'^series/(?P<serie_id>\d+)/(?P<season>\d+)/(?P<episode>\d+)/$', episode_resource, name='API_v1_episode_detail'),
)
