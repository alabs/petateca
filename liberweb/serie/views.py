from django.http import HttpResponse

def index(request):
    return HttpResponse('Listado de series')

def get_serie(request, serie_slug):
    return HttpResponse("Hola, soy la serie: %s" % serie_slug)

def get_episodes(request, serie_slug):
    return HttpResponse('Listado de episodios')

def get_episode(request, serie_slug, episode_slug):
    return HttpResponse("Hola, soy el episodio: %s" % episode_slug)

