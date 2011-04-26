
from serie.models import Serie, Episode, Actor, Role, Season, ImageSerie, ImageActor

from decorators import render_to

@render_to('serie/ajax_serie.html')
def serie_lookup(request, serie_id):
    ''' JQuery PopUp en las imagenes '''
    serie = Serie.objects.get(id=serie_id)
    genres = serie.genres.all()
    return { 'serie' : serie, 'genres': genres }


@render_to('serie/ajax_season.html')
def season_lookup(request, serie_id, season):
    serie = Serie.objects.get(id=serie_id)
    season = Season.objects.get(serie=serie, season=season)
    episode_list = season.episodes.all().order_by('episode')
    return { 
        'episode_list' : episode_list,
    }


@render_to('serie/ajax_actors.html')
def actors_lookup(request, serie_slug):
    serie = Serie.objects.get(slug_name=serie_slug)
    roles = Role.objects.select_related('actor', 'serie', 'actor__poster').filter(serie = serie)
    return { 'roles': roles }


@render_to('serie/generic_list.html')
def ajax_letter(request, letter):
    series = Serie.objects.filter(name__startswith=letter)
    return { 'series_list': series }


@render_to('serie/generic_list.html')
def ajax_genre(request, genre_slug):
    genre = Genre.objects.get(slug_name = genre_slug)
    return { 'series_list': genre.series.all() }


@render_to('serie/generic_list.html')
def ajax_network(request, network_slug):
    network = Network.objects.get(slug_name = network_slug)
    return { 'series_list': network.series.all() }
