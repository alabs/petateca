from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from core.decorators import render_to

from serie import models as m 


@login_required
def set_tracking(request):
    """
    Tracking / Seguimiento de las series. 

    Recibo un episodio (con su serie y temporada) y lo marco como visto
    Antes, reviso los episodios ya vistos y compruebo que no sea para 
    esta misma serie, si ya tiene uno visto, lo quito.
    """
    if request.method == 'POST' and request.is_ajax():
        episode_n = int(request.POST['episode'])
        season_n = int(request.POST['season'])
        user = request.user
        serie = m.Serie.objects.get(id=int(request.POST['serie_id']))
        season = m.Season.objects.get(serie=serie, season=season_n)
        episode = m.Episode.objects.get(season=season, episode=episode_n)
        # clean old episodes viewed for this serie
        episodes_viewed = user.profile.viewed_episodes.all()
        for epi in episodes_viewed:
            if epi.season.serie == serie:
                epi.viewed_episodes.remove(user.profile)
        # mark episode as viewed
        episode.viewed_episodes.add(user.profile)
        return HttpResponse(
            simplejson.dumps('OK'), 
            mimetype='application/json'
        )
    else:
        return HttpResponseForbidden('Error en la peticion AJAX')


@render_to('tracking/show_tracking.html')
def show_tracking(request):
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        serie = request.POST.get('serie_id')
        episode = user.profile.viewed_episodes.get(season__serie=serie)
        episodes = episode.get_next_5_episodes()
        return { 'episodes': episodes }
    else:
        return HttpResponseForbidden('Error en la peticion AJAX')
