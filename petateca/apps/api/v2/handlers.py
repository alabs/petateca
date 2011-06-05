from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from piston.handler import BaseHandler

from serie.models import Serie, Season, Episode
from api.utils import catch_404

current_site = Site.objects.get_current()
urlprefix = 'http://' + current_site.domain



class SerieListHandler(BaseHandler):
    ''' Listado de series '''
    allowed_methods = ('GET', )
    model = Serie

    @catch_404
    def read(self, request):
        ''' Muestra listado de series con URL para ver detalle ''' 
        series = Serie.objects.order_by('name_es')
        serie_list = []
        for s in series:
            serie_list.append({
                'name': s.name,
                'id': s.pk,
                'url': urlprefix + reverse('API_serie_detail', 
                    kwargs={'serie_id': s.pk})
                })
        return serie_list


class SerieHandler(BaseHandler):
    ''' Detalle de Serie '''
    allowed_methods = ('GET', )
    model = Serie
    fields = ('id', 'name', 'slug', 'description', ('network', ('name', )), 
            'runtime', ('genres', ('name', )), 'rating_score', )

    @catch_404
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
        return get_object_or_404(Serie, id=serie_id)


# TODO: Actores, Posters, Posters de Actores
# /posters
# /actors

class SeasonListHandler(BaseHandler):
    ''' Listado de temporadas '''
    allowed_methods = ('GET', )
    model = Season

    @catch_404
    def read(self, request, serie_id):
        ''' Muestra el listado de URLs de temporadas que tiene una Serie'''
        serie = get_object_or_404(Serie, id=serie_id)
        season_list = []
        for s in serie.season.all():
            season_list.append({
                'id': s.pk,
                'url': urlprefix + reverse('API_season_detail', 
                    kwargs={'serie_id': serie.id, 'season': s.season}),
                })
        # TODO: Imagen de Temporadas
        return season_list


class SeasonHandler(BaseHandler):
    ''' Detalle de temporada '''
    allowed_methods = ('GET', )
    model = Season

    @catch_404
    def read(self, request, serie_id, season):
        ''' Muestra el listado de episodios para una temporada dada, y lista la siguiente informacion de cada episodio: 

        * Titulo: 'title'
        * Fecha de emision: 'air_date'
        * Ubicacion del recurso del episodio: 'url'
        '''
        serie = get_object_or_404(Serie, id=serie_id)
        season = get_object_or_404(Season, serie=serie, season=season) 
        epi_list = []
        for e in season.episodes.all():
            # TODO: season y serie
            epi = {
                    'episode': e.episode,
                    'title' : e.title,
                    'url': urlprefix + reverse("API_episode_detail", kwargs={
                        'serie_id': serie.id, 'season': season.season, 'episode': e.episode}),
                    }
            if e.air_date: 
                epi['air_date'] = e.air_date.isoformat()
            epi_list.append(epi)
        return epi_list


class EpisodeHandler(BaseHandler):
    ''' Detalle de episodio '''
    allowed_methods = ('GET', )
    model = Episode

    @catch_404
    def read(self, request, serie_id, season, episode):
        ''' Muestra la informacion de un episodio:

        * Titulo: 'title' 
        * Numero de Episodio: 'episode'
        * Numero de Temporada: 'season'
        * Fecha de Emision: 'air_date'
        * Listado de URLs
        '''
        serie = get_object_or_404(Serie, id=serie_id)
        season = get_object_or_404(Season, serie=serie, season=season) 
        epi = get_object_or_404(Episode, season=season, episode=episode)
        # TODO: Imagen de episodio
        episode = {
                'id': epi.pk,
                'season': season.season,
                'episode': epi.episode,
                'title': epi.title,
                'air_date': epi.air_date.isoformat(),
                }
        link_list = []
        for l in epi.links.all():
            link = {'url': l.url, 'audio': l.audio_lang.iso_code,}
            if l.subtitle: 
                link['subtitle'] = l.subtitle.iso_code
            link_list.append(link)
        episode['links'] = link_list
        return episode
