# pylint: disable-msg=E1102
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from djangoratings.views import AddRatingView
from decorators import render_to
from lib.namepaginator import NamePaginator
from serie.forms import LinkForm
from serie.models import Genre, Network, Link, Languages
from serie.models import Serie, Episode, Actor, Role, Season
from voting.models import Vote


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
    seasons = serie.season.all().order_by('season')
    score = int(round(serie.rating.get_rating()))
    # Vemos si el usuario tiene la serie como favorita
    try:
        serie.favorite_of.get(user=request.user.profile)
        favorite_status = 'yes'
    except:
        favorite_status = 'no'
    serie_title = serie.name.title()
    # Preparamos serie_info con la serie, titulo, imagenes, episodios...
    serie_info = {
        'serie': serie,
        'title': serie_title,
        'image': img_src,
        'season_list': seasons,
        'score': score,
        'favorite': favorite_status,
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
            if request.POST.has_key('rating'):
                # Si el usuario esta autenticado, prepara el voto
                content_type = ContentType.objects.get(app_label='serie', name='serie')
                params = {
                    'content_type_id': content_type.id,
                    'object_id': serie.id,
                    'field_name': 'rating',  # campo en el modelo
                    'score': request.POST['rating'],
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
                    'favorite': 'yes',
                })
            elif request.POST.has_key('no-favorite'):
                user = User.objects.get(username=request.user)
                serie.favorite_of.remove(user.profile)
                serie_info.update({
                    'favorite': 'no',
                })
        return serie_info


@render_to('serie/get_season.html')
def get_season(request, serie_slug, season):
    ''' Get season, returns episode_list
    also handles link voting (courtesy of django-voting) '''
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    season = get_object_or_404(Season, serie=serie, season=season)
    episode_list = Episode.objects.filter(
        season=season,
    ).order_by('episode')
    season_info = {
        'serie': serie,
        'episode_list': episode_list,
        'season': season,
    }

    if request.method == 'GET':
        return season_info
    if request.method == 'POST':
        if not request.user.is_authenticated():
            season_info.update({
                'message': 'No registrado',
            })
            return season_info
        user = User.objects.get(username=request.user)
        link = Link.objects.get(id=request.POST['linkid'])
        if request.POST['vote'] == 'upvote':
            Vote.objects.record_vote(link, user, +1)
        elif request.POST['vote'] == 'downvote':
            Vote.objects.record_vote(link, user, -1)
        return season_info


@render_to('serie/get_episode.html')
def get_episode(request, serie_slug, season, episode):
    ''' Get the episode itsef ''' 
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    season = get_object_or_404(Season, serie=serie, season=season)
    episode = get_object_or_404(
        Episode,
        season=season,
        episode=episode
    )
    episode_info = {
        'serie': serie,
        'episode': episode,
        'season': season,
    }
    if request.method == 'GET':
        return episode_info
    if request.method == 'POST':
        if not request.user.is_authenticated():
            episode_info.update({
                'message': 'No registrado',
            })
            return episode_info
        user = User.objects.get(username=request.user)
        link = Link.objects.get(id=request.POST['linkid'])
        if request.POST['vote'] == 'upvote':
            Vote.objects.record_vote(link, user, +1)
        elif request.POST['vote'] == 'downvote':
            Vote.objects.record_vote(link, user, -1)
        episode_info.update({
            'message': 'Vote recorded',
        })
        return episode_info


@render_to('serie/list_popular.html')
def list_popular(request):
    series = Serie.objects.all()
    popular_series = series.order_by('-rating_score')
    return { 'series': popular_series }


def list_user_recommendation(request):
    return "TODO: listar las recomendaciones para el usuario"

# FIXME: probablemente todas estas cosas tan repetitivas y estupidas
# sean por lo que existe el object_list en el url.


@render_to('serie/get_actor.html')
def get_actor(request, slug_name):
    actor = get_object_or_404(Actor, slug_name=slug_name)
    role = get_object_or_404(Role, actor=actor)
    imgs = actor.images.all()
    img_src = imgs[0].src if imgs else None
    return {
        'actor': actor,
        'title': actor.name,
        'role': role,
        'image': img_src,
    }


# SERIES_LIST: todas van a serie_list 

@render_to('serie/serie_list.html')
def get_genre(request, slug_name):
    genre_list = Genre.objects.order_by('name').all()
    network_list = Network.objects.order_by('name').all()
    genre = get_object_or_404(Genre, slug_name=slug_name)
    serie_list = Serie.objects.filter(genres=genre.id)
    serie_list = serie_list.order_by("name")
    paginator = NamePaginator(
        serie_list,
        on="name",
        per_page = 10
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
        'genre': genre,
        'page': page,
        'genre_list': genre_list,
        'network_list': network_list,
    }


@render_to('serie/serie_list.html')
def get_network(request, slug_name):
    genre_list = Genre.objects.order_by('name').all()
    network_list = Network.objects.order_by('name').all()
    network = get_object_or_404(Network, slug_name=slug_name)
    serie_list = Serie.objects.filter(network=network.id)
    serie_list = serie_list.order_by("name")
    paginator = NamePaginator(
        serie_list,
        on="name",
        per_page = 10
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
        'network': network,
        'page': page,
        'genre_list': genre_list,
        'network_list': network_list,
    }


@render_to('serie/serie_list.html')
def get_serie_list(request):
    genre_list = Genre.objects.order_by('name').all()
    network_list = Network.objects.order_by('name').all()
    serie_list = Serie.objects.order_by('name').all()
    paginator = NamePaginator(
        serie_list,
        on="name",
        per_page = 10
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
        'genre_list': genre_list,
        'network_list': network_list,
    }


@login_required
@render_to('serie/add_link.html')
def add_link(request, serie_slug, season, episode):
    ''' 
    Formulario que agrega/edita links
    ''' 
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    season = get_object_or_404(Season, serie=serie, season=season)
    episode = get_object_or_404(
        Episode,
        season=season,
        episode=episode
    )
    link_info = {
        'serie': serie,
        'episode': episode,
        'season': season,
    }
    if request.method == 'POST':
        # Capturamos lo que nos pasa, agregamos el episode
        # fecha de publicacion y usuario que hace la peticion
        data = {
            'url': request.POST['url'],
            'audio_lang': request.POST['audio_lang'],
            'subtitle': request.POST['subtitle'],
            'user': request.user.username,
            'episode': episode.pk,
            'pub_date': datetime.now(),
        }
        form = LinkForm(data)
        link_info.update({'form': form})
        if form.is_valid():
            if not data['url'].startswith('http://'):
                link_info.update({ 'message': 'URL Invalida',})
                return link_info
            # Audio Lang, Subtitle y Episode hay que pasarlos como instancias
            # Episode ya lo tenemos, vamos a buscar audio_lang
            lang = Languages.objects.get(pk=data['audio_lang'])
            link = Link(
                url=data['url'],
                audio_lang=lang,
                user=data['user'],
                episode=episode,
                pub_date=data['pub_date'],
            )
            # En caso de tener subtitulos, los tratamos
            if data['subtitle']:
                subt = Languages.objects.get(pk=data['subtitle'])
                link.subtitle = subt
            link.save()
            link_info.update({ 'message': 'Gracias',})
            return link_info
        else:
            link_info.update({ 'message': 'Error',})
            return link_info
    else:
        # Este es el formulario inicial, si el request.method es GET
        # pre-populamos con el episodio, que eso ya lo tenemos de la URL
        form = LinkForm(initial={'episode':episode}) 
        link_info.update({'form': form,})
    return link_info
