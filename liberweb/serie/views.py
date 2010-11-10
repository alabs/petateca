from liberweb.serie.models import Serie, Episode
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse

from django.utils.translation import gettext_lazy as _

def get_serie(request, serie_slug):
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    img = serie.images.get()
    return render_to_response('serie/get_serie.html', {
        'serie': serie,
        'title': serie.name,
        'image': img.src,
    })

def get_episodes(request, serie_slug):
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    return render_to_response('serie/get_episodes.html', {
        'serie': serie,
        'title': _("Episodes of %(name)s") % {"name": serie.name}, 
    })

def get_episode(request, serie_slug, episode_slug):
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    episode = get_object_or_404(Episode, slug_title=episode_slug)
    return render_to_response('serie/get_episode.html', {'serie': serie, 'episode': episode })

def list_user_favorite(request):
    return "TODO"

def list_user_recommendation(request):
    return "TODO"

def index(request):
    ctx = {}
    return render_to_response('serie/index.html', ctx)
