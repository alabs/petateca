from django.conf.urls.defaults import *

from piston.doc import documentation_view 
from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource

from api.handlers import SerieListHandler, SerieHandler, SeasonListHandler, SeasonHandler, EpisodeHandler

auth = HttpBasicAuthentication(realm="Liberateca API - Autenticacion")
ad = { 'authentication': auth }

serielist_resource = Resource(handler=SerieListHandler, **ad)
serie_resource = Resource(handler=SerieHandler, **ad)
seasonlist_resource = Resource(handler=SeasonListHandler, **ad)
season_resource = Resource(handler=SeasonHandler, **ad)
episode_resource = Resource(handler=EpisodeHandler, **ad)

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'api.html'}),
    url(r'^series/$', serielist_resource, name='API_serie_list'),
    url(r'^series/(?P<serie_id>\d+)/$', serie_resource, name='API_serie_detail'),
    url(r'^series/(?P<serie_id>\d+)/seasons/$', seasonlist_resource, name='API_season_list'),
    url(r'^series/(?P<serie_id>\d+)/(?P<season>\d+)/$', season_resource, name='API_season_detail'),
    url(r'^series/(?P<serie_id>\d+)/(?P<season>\d+)/(?P<episode>\d+)/$', episode_resource, name='API_episode_detail'),
)
