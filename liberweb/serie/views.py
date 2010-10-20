from liberweb.serie.models import Serie, Episode
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse

def index(request):
    series = Serie.objects.all()
    return render_to_response('serie/index.html', {'series': series})

def get_serie(request, serie_slug):
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    return render_to_response('serie/get_serie.html', {'serie': serie})

def get_episodes(request, serie_slug):
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    return render_to_response('serie/get_episodes.html', {'serie': serie})

def get_episode(request, serie_slug, episode_slug):
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    episode = get_object_or_404(Episode, slug_title=episode_slug)
    return render_to_response('serie/get_episode.html', {'serie': serie, 'episode': episode })

def by_date(request):
    return "TODO"

def by_popularity(request):
    return "TODO"

def by_review(request):
    return "TODO"
