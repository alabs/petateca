from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from serie.models import Serie, Season, Episode

current_site = Site.objects.get_current()
urlprefix = 'http://' + current_site.domain

class SerieListHandler(BaseHandler):
    allowed_methods = ('GET', )

    def read(self, request):
        series = Serie.objects.all()
        serie_list = []
        for s in series:
            serie = {}
            serie['name'] = s.name
            serie['url'] = urlprefix + reverse("API_serie_detail", kwargs=dict(serie_id=s.id))
            serie_list.append(serie)
        return serie_list


class SerieHandler(BaseHandler):
    allowed_methods = ('GET', )
    fields = ('id', 'name', 'slug', 'description', ('network', ('name', )), 'runtime', ('genres', ('name', )), 'rating_score', )
    model = Serie

    def read(self, request, serie_id):
        serie = get_object_or_404(Serie, id=serie_id)
        return serie


class SeasonListHandler(BaseHandler):
    allowed_methods = ('GET', )

    def read(self, request, serie_id):
        serie = get_object_or_404(Serie, id=serie_id)
        season_list = []
        for s in serie.season.all():
            season_list.append(urlprefix + reverse("API_season_detail", kwargs=dict(serie_id=serie.id, season=s.season)))
        # TODO: url de SeasonHandler
        return { 'seasons': season_list }


class SeasonHandler(BaseHandler):
    allowed_methods = ('GET', )

    def read(self, request, serie_id, season):
        serie = get_object_or_404(Serie, id=serie_id)
        season = get_object_or_404(Season, serie=serie, season=season) 
        epi_list = []
        for e in season.episodes.all():
            # TODO: url de EpisodeHandler
            epi = {}
            epi['episode'] = e.episode 
            epi['title'] = e.title
            if e.air_date: epi['air_date'] = e.air_date.isoformat()
            epi['url'] = urlprefix + reverse("API_episode_detail", kwargs=dict(serie_id=serie.id, season=season.season, episode=e.episode))
            epi_list.append(epi)
        return epi_list


class EpisodeHandler(BaseHandler):
    allowed_methods = ('GET', )

    def read(self, request, serie_id, season, episode):
        serie = get_object_or_404(Serie, id=serie_id)
        season = get_object_or_404(Season, serie=serie, season=season) 
        epi = get_object_or_404(Episode, season=season, episode=episode)
        episode = {}
        episode['season'] = season.season
        episode['episode'] = epi.episode
        episode['title'] = epi.title
        link_list = []
        for l in epi.links.all():
            link = {}
            link['url'] = l.url
            link['audio'] = l.audio_lang.iso_code
            if l.subtitle: link['subtitle'] = l.subtitle.iso_code
            link_list.append(link)
        episode['links'] = link_list
        return episode
