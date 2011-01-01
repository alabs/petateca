from liberweb.serie.models import Serie, Episode, Actor, Role
from liberweb.serie.models import Genre, Network, Link
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from django.core.paginator import InvalidPage, EmptyPage
from liberweb.lib.namepaginator import NamePaginator

from djangoratings.views import AddRatingView
from django.views.decorators.csrf import csrf_protect
from django.contrib.contenttypes.models import ContentType

# Un atajo para que el return sea solo el diccionario
# Mete el RequestContext
from liberweb.decorators import render_to

from django.contrib.auth.models import User
from voting.models import Vote


@render_to('serie/serie_list.html')
def get_serie_list(request):
    serie_list = Serie.objects.order_by('name').all()
    paginator = NamePaginator(
        serie_list,
        on="name",
        per_page=25
    )

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    return {
        'page': page,
    }


@render_to('serie/get_serie.html')
@csrf_protect
def get_serie(request, serie_slug):
    ''' Request a serie, returns images and episodes,
    also treats star-rating, courtesy of django-ratings'''
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    imgs = serie.images.filter(is_poster=True)
    img_src = imgs[0].src if imgs else None
    #episodes = serie.episodes.all().order_by('season')
    # Hacemos un listado de las temporadas:
    seasons = list(set(
        [epi.season for epi in serie.episodes.all().order_by('season')]
    ))
    score = int(round(serie.rating_user.get_rating()))
    # Preparamos serie_info con la serie, titulo, imagenes, episodios...
    serie_info = {
        'serie': serie,
        'title': serie.name,
        'image': img_src,
        'season_list': seasons,
        'score': score,
    }
    # Si el metodo es GET devuelve serie_info asi nomas
    if request.method == 'GET':
        return serie_info
    # si es POST trata el rating:
    if request.method == 'POST':
        if not request.user.is_authenticated():
            serie_info.update({
                'message': 'No registrado',
            })
        else:
            if request.POST.has_key('user_rating'):
                # Si el usuario esta autenticado, prepara el voto
                ct = ContentType.objects.get(app_label='serie', name='serie')
                params = {
                    'content_type_id': ct.id,
                    'object_id': serie.id,
                    'field_name': 'rating_user',  # campo en el modelo
                    'score': request.POST['user_rating'],
                }
                response = AddRatingView()(request, **params)
                try:
                # Distintas respuestas a la peticion: grabado, Ya ha votado, Error
                    if response.content == 'Vote recorded':
                        serie_info.update({
                            'message': 'Vote recorded',
                            'score': params['score'],
                        })
                    elif response.content == 'You have already voted.':
                        serie_info.update({
                                'message': 'You have already voted',
                        })
                except:
                    serie_info.update({
                        'message': response.content,
                        'error': 9,
                    })
            elif request.POST.has_key('favorite'):
                user = User.objects.get(username=request.user)
                serie.favorite_of.add(user.profile)
                serie_info.update({
                    'favorite': 'successful',
                })
        return serie_info


@render_to('serie/get_season.html')
def get_season(request, serie_slug, season):
    ''' Get season, returns episode_list
    also handles link voting (courtesy of django-voting) '''
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    episode_list = Episode.objects.filter(
        season=season,
        serie=serie
    ).order_by('episode')
    season_info = {
        'serie': serie,
        'episode_list': episode_list,
    }

    if request.method == 'GET':
        return season_info
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        link = Link.objects.get(id=request.POST['linkid'])
        if request.POST['vote'] == 'upvote':
            Vote.objects.record_vote(link, user, +1)
        elif request.POST['vote'] == 'downvote':
            Vote.objects.record_vote(link, user, -1)
        return season_info


@render_to('serie/get_episodes.html')
# DEPRECATED, ahora se tira de get_season
def get_episodes(request, serie_slug):
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    episodes = serie.episodes.all().order_by('season')
    return {
        'serie': serie,
        'episode_list': episodes,
        'title': _("Episodes of %(name)s") % {"name": serie.name},
    }


@render_to('serie/get_episode.html')
# Es Interesnte tener una ficha por episodio?? dejo la pregunta en el aire
def get_episode(request, serie_slug, season, episode):
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    episode = get_object_or_404(
        Episode,
        serie=serie,
        season=season,
        episode=episode
    )
    return {
        'serie': serie,
        'episode': episode,
    }


def list_user_favorite(request):
    return "TODO: listar las favoritas del usuario"


def list_user_recommendation(request):
    return "TODO: listar las recomendaciones para el usuario"

# FIXME: probablemente todas estas cosas tan repetitivas y estupidas
# sean por lo que existe el object_list en el url.


@render_to('serie/get_actor.html')
def get_actor(request, slug_name):
    a = get_object_or_404(Actor, slug_name=slug_name)
    role = get_object_or_404(Role, actor=a)
    imgs = a.images.all()
    img_src = imgs[0].src if imgs else None
    return {
        'actor': a,
        'title': a.name,
        'role': role,
        'image': img_src,
    }


@render_to('serie/get_genre.html')
def get_genre(request, slug_name):
    genre = get_object_or_404(Genre, slug_name=slug_name)
    serie_list = Serie.objects.filter(genres=genre.id)
    serie_list = serie_list.order_by("name")
    return {
        'genre': genre,
        'serie_list': serie_list,
    }


@render_to('serie/get_network.html')
def get_network(request, slug_name):
    network = get_object_or_404(Network, slug_name=slug_name)
    serie_list = Serie.objects.filter(network=network.id)
    serie_list = serie_list.order_by("name")
    return {
        'network': network,
        'serie_list': serie_list,
    }
