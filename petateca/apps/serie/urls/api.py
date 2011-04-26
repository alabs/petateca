from django.conf.urls.defaults import *

from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource
from serie.handlers import SerieListHandler, SerieHandler, SeasonListHandler, SeasonHandler, EpisodeHandler

auth = HttpBasicAuthentication(realm="Liberateca API - Autenticacion")
ad = { 'authentication': auth }

serielist_resource = Resource(handler=SerieListHandler, **ad)
serie_resource = Resource(handler=SerieHandler, **ad)
seasonlist_resource = Resource(handler=SeasonListHandler, **ad)
season_resource = Resource(handler=SeasonHandler, **ad)
episode_resource = Resource(handler=EpisodeHandler, **ad)


urlpatterns = patterns('',
    url(r'^/serie$', serielist_resource),
    url(r'^/serie/(?P<serie_id>\d+)$', serie_resource, name='API_serie_detail'),
    url(r'^/serie/(?P<serie_id>\d+)/seasons$', seasonlist_resource),
    url(r'^/serie/(?P<serie_id>\d+)/(?P<season>\d+)$', season_resource, name='API_season_detail'),
    url(r'^/serie/(?P<serie_id>\d+)/(?P<season>\d+)/(?P<episode>\d+)$', episode_resource, name='API_episode_detail'),
)
