from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson

from serie.models import Serie, Season, Episode

current_site = Site.objects.get_current()
urlprefix = 'http://' + current_site.domain


def series_list(request):
    ''' Devuelve listado de series e id '''
    series = Serie.objects.all().order_by('name')
    all_series = []
    for serie in series:
        series_list = {}
        series_list['name'] = serie.name
        series_list['url'] = urlprefix + reverse("API_serie_detail", kwargs=dict(id_serie=serie.id))
        all_series.append(series_list)
    return HttpResponse(simplejson.dumps(all_series, indent=4, ensure_ascii=False), mimetype='application/json')


def serie_detail(request, id_serie):
    ''' Devuelve la informacion de la serie '''
    serie = get_object_or_404(Serie, id=id_serie)
    current_site = Site.objects.get_current()
    genre_list = []
    for genre in serie.genres.all(): genre_list.append(genre.name)
    serie_info = {}
    serie_info['name'] = serie.name
    serie_info['slug'] = serie.get_absolute_url()
    serie_info['id'] = serie.id
    serie_info['description'] = serie.description
    serie_info['network'] = serie.network.name
    serie_info['runtime'] = serie.runtime
    serie_info['genres'] = genre_list
    serie_info['rating'] = serie.rating.score
    # TODO: Actors, Poster
    season_list = []
    for s in serie.season.all():
        season_list.append(urlprefix + reverse("API_season_detail", kwargs=dict(id_serie=serie.id, season=s.season)))
    serie_info['seasons'] = season_list
    return HttpResponse(simplejson.dumps(serie_info, indent=4, ensure_ascii=False), mimetype='application/json')


def season_detail(request, id_serie, season):
    ''' Devuelve el listado de episodios con id '''
    season = get_object_or_404(Season, serie=Serie.objects.get(id=id_serie), season=season)
    epi_list = []
    for e in season.episodes.all():
        epi = {}
        epi['episode'] = urlprefix + reverse("API_episode_detail", kwargs=dict(id_serie=season.serie.id, season=season.season, episode=e.episode))
        epi['title'] = e.title.encode('latin-1')
        if e.air_date: epi['air_date'] = e.air_date.isoformat()
        epi['slug'] = e.get_absolute_url()
        epi_list.append(epi)
    return HttpResponse(simplejson.dumps(epi_list, indent=4, ensure_ascii=False), mimetype='application/json')


def episode_detail(request, id_serie, season, episode):
    ''' Devuelve los links de un episodio con su informacion '''
    season = get_object_or_404(Season, serie=Serie.objects.get(id=id_serie), season=season)
    epi_detail = []
    for epi in season.episodes.all():
        episode = {}
        episode['season'] = season.season
        episode['episode'] = epi.episode
        episode['title'] = epi.title
        episode['url'] = urlprefix + epi.get_absolute_url()
        link_list = []
        for l in epi.links.all():
            link = {}
            link['url'] = l.url
            link['audio'] = l.audio_lang.iso_code
            if l.subtitle: link['subtitle'] = l.subtitle.iso_code
            link_list.append(link)
        episode['links'] = link_list
        epi_detail.append(episode)
    return HttpResponse(simplejson.dumps(epi_detail, indent=4, ensure_ascii=False), mimetype='application/json')


