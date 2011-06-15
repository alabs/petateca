from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from piston.handler import BaseHandler

from serie.models import Serie, Season, Episode
from api_v2.utils import catch_404, get_urlprefix

urlprefix = get_urlprefix()



class SerieListHandler(BaseHandler):
    ''' Listado de series '''
    allowed_methods = ('GET', )
    model = Serie
    fields = ('id', 'name_en', 'name_es', 'url')

    @catch_404
    def read(self, request):
        ''' Muestra listado de series con URL para ver detalle ''' 
        series = Serie.objects.order_by('name_es')
        return series


class SerieHandler(BaseHandler):
    ''' Detalle de Serie '''
    allowed_methods = ('GET', )
    model = Serie
    fields = ('id', 'name_es', 'name_en', 'slug', 'description_en', 'description_es', 
            ('network', ('name', )), 'runtime', ('genres', ('name', )), 
            'rating_score', ( 'poster', ('thumbnail', )), )


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
        * Thumbnail: 'poster'
        '''
        return get_object_or_404(Serie, id=serie_id)


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
                'url': urlprefix + reverse('API_v2_season_detail', 
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
                    'url': urlprefix + reverse("API_v2_episode_detail", kwargs={
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
                'title_es': epi.title_es,
                'title_en': epi.title_en,
                'description_en': epi.description_en,
                'description_es': epi.description_es,
                'air_date': epi.air_date.isoformat(),
                }
        try:
            episode['thumbnail'] = epi.poster.thumbnail()
        except:
            pass
        link_list = []
        for l in epi.links.all():
            link = {'url': l.url, 'audio': l.audio_lang.iso_code,}
            if l.subtitle: 
                link['subtitle'] = l.subtitle.iso_code
            link_list.append(link)
        episode['links'] = link_list
        return episode
