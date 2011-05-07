from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404

from piston.handler import BaseHandler
from piston.utils import rc, throttle
from piston.doc import generate_doc

from serie.models import Serie, Season, Episode

current_site = Site.objects.get_current()
urlprefix = 'http://' + current_site.domain

class SerieListHandler(BaseHandler):
    ''' Listado de series '''
    allowed_methods = ('GET', )
    model = Serie

    def read(self, request):
        ''' Muestra listado de series con URL para ver detalle ''' 
        series = Serie.objects.all()
        serie_list = []
        for s in series:
            serie = {}
            serie['name'] = s.name
            serie['url'] = urlprefix + reverse("API_serie_detail", kwargs=dict(serie_id=s.id))
            serie['id'] = s.id
            serie_list.append(serie)
        return serie_list


class SerieHandler(BaseHandler):
    ''' Detalle de Serie '''
    allowed_methods = ('GET', )
    fields = ('id', 'name', 'slug', 'description', ('network', ('name', )), 'runtime', ('genres', ('name', )), 'rating_score', )
    model = Serie

    def read(self, request, serie_id):
        ''' Muestra el detalle de la serie: 

        * Nombre: 'name'
        * URL: 'slug'
        * Descripcion: 'description'
        * Cadena: 'network'
        * Duracion: 'runtime'
        * Generos: 'genre'
        * Puntuacion: 'rating_score'
        '''
        try: 
            serie = get_object_or_404(Serie, id=serie_id)
        except Http404:
            return rc.NOT_FOUND 
        return serie


# TODO: Actores, Posters, Posters de Actores
# /posters
# /actors

class SeasonListHandler(BaseHandler):
    ''' Listado de temporadas '''
    allowed_methods = ('GET', )
    model = Season

    def read(self, request, serie_id):
        ''' Muestra el listado de URLs de temporadas que tiene una Serie'''
        try: 
            serie = get_object_or_404(Serie, id=serie_id)
        except Http404:
            return rc.NOT_FOUND 
        season_list = []
        for s in serie.season.all():
            season_list.append(urlprefix + reverse("API_season_detail", kwargs=dict(serie_id=serie.id, season=s.season)))
        # TODO: Imagen de Temporadas
        return { 'seasons': season_list }



class SeasonHandler(BaseHandler):
    ''' Detalle de temporada '''
    allowed_methods = ('GET', )
    model = Season

    def read(self, request, serie_id, season):
        ''' Muestra el listado de episodios para una temporada dada, y lista la siguiente informacion de cada episodio: 

        * Titulo: 'title'
        * Fecha de emision: 'air_date'
        * Ubicacion del recurso del episodio: 'url'
        '''
        try: 
            serie = get_object_or_404(Serie, id=serie_id)
            season = get_object_or_404(Season, serie=serie, season=season) 
        except Http404:
            return rc.NOT_FOUND 
        epi_list = []
        for e in season.episodes.all():
            # TODO: season y serie
            epi = {}
            epi['episode'] = e.episode 
            epi['title'] = e.title
            if e.air_date: epi['air_date'] = e.air_date.isoformat()
            epi['url'] = urlprefix + reverse("API_episode_detail", kwargs=dict(serie_id=serie.id, season=season.season, episode=e.episode))
            epi_list.append(epi)
        return epi_list



class EpisodeHandler(BaseHandler):
    ''' Detalle de episodio '''
    allowed_methods = ('GET', )
    model = Episode

    def read(self, request, serie_id, season, episode):
        ''' Muestra la informacion de un episodio:

        * Titulo: 'title' 
        * Numero de Episodio: 'episode'
        * Numero de Temporada: 'season'
        * Fecha de Emision: 'air_date'
        * Listado de URLs
        '''
        try: 
            serie = get_object_or_404(Serie, id=serie_id)
            season = get_object_or_404(Season, serie=serie, season=season) 
            epi = get_object_or_404(Episode, season=season, episode=episode)
        except Http404:
            return rc.NOT_FOUND 
        episode = {}
        # TODO: Imagen de episodio
        episode['season'] = season.season
        episode['episode'] = epi.episode
        episode['title'] = epi.title
        episode['air_date'] = epi.air_date.isoformat()
        link_list = []
        for l in epi.links.all():
            link = {}
            link['url'] = l.url
            link['audio'] = l.audio_lang.iso_code
            if l.subtitle: link['subtitle'] = l.subtitle.iso_code
            link_list.append(link)
        episode['links'] = link_list
        return episode

