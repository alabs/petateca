# pylint: disable-msg=E1102

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.paginator import InvalidPage, EmptyPage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from djangoratings.views import AddRatingView
from voting.models import Vote

from serie.forms import LinkForm
from serie.models import Genre, Network, Link, Languages
from serie.models import Serie, Episode, Actor, Role, Season, ImageSerie, ImageActor

from datetime import datetime
from lib.namepaginator import NamePaginator
from decorators import render_to


@render_to('serie/get_serie.html')
@csrf_protect
def get_serie(request, serie_slug):
    ''' Request a serie, returns images and episodes,
    also treats star-rating, courtesy of django-ratings'''
    serie = get_object_or_404(Serie.objects.select_related(), slug_name=serie_slug)
    # Vemos si el usuario tiene la serie como favorita
    try:
        serie.favorite_of.get(user=request.user.profile)
        favorite_status = 'yes'
    except:
        favorite_status = 'no'
    # Si el metodo es GET devuelve serie_info asi nomas
    if request.method == 'GET':
        # Preparamos serie_info con la serie, titulo, imagenes, episodios...
        serie_info = {
            'serie': serie,
            'title': serie.name.title(),
            'season_list': Season.objects.select_related('poster', 'serie').filter(serie=serie).order_by('season'),
            'score': int(round(serie.rating.get_rating())),
            'favorite': favorite_status,
            'roles': Role.objects.select_related('actor', 'serie', 'actor__poster').filter(serie = serie),
        }
        return serie_info
    # si es POST trata el favorito/rating:
    if request.method == 'POST' and request.is_ajax():
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user)
            # Si es favorito (corazon)
            if request.POST.has_key('favorite'):
                serie.favorite_of.add(user.profile)
                return HttpResponse(simplejson.dumps('yes'), mimetype='application/json')
            elif request.POST.has_key('no-favorite'):
                serie.favorite_of.remove(user.profile)
                return HttpResponse(simplejson.dumps('no'), mimetype='application/json')
            # Si es rating de estrellas
            if request.POST.has_key('rating'):
                content_type = ContentType.objects.get(app_label='serie', name='serie')
                params = {
                    'content_type_id': content_type.id,
                    'object_id': serie.id,
                    'field_name': 'rating',  # campo en el modelo
                    'score': request.POST['rating'],
                }
                response = AddRatingView()(request, **params)
                return HttpResponse(simplejson.dumps(response.content), mimetype='application/json')
        else: 
            # El usuario no esta autenticado
            return HttpResponse(simplejson.dumps('no-user'), mimetype='application/json')


@render_to('serie/get_season.html')
def get_season(request, serie_slug, season):
    ''' Get season, returns episode_list '''
    episode_list = Episode.objects.select_related('poster', 'season', 'season__serie'). \
                    filter(season__season=season, season__serie__slug_name=serie_slug).order_by('episode')
    if episode_list:
        season = episode_list[0].season
    else:
        season = get_object_or_404(Season.objects.select_related(), serie__slug_name=serie_slug, season=season)
    serie = season.serie
    season_info = {
        'serie': serie,
        'episode_list': episode_list,
        'season': season,
        'next_season': season.get_next_season(),
        'prev_season': season.get_previous_season(),
    }
    return season_info


@csrf_protect
@render_to('serie/get_episode.html')
def get_episode(request, serie_slug, season, episode):
    ''' Get the episode itsef ''' 
    episode = get_object_or_404(
        Episode.objects.select_related('season', 'season__serie', 'poster'),
        season__season = season,
        season__serie__slug_name = serie_slug,
        episode=episode
    )
    season = episode.season
    serie = season.serie
    episode_info = {
        'serie': serie,
        'episode': episode,
        'season': season,
        'link_list': Link.objects.select_related().filter(episode=episode),
        'next_epi': episode.get_next_episode(),
        'prev_epi': episode.get_previous_episode(),
    }
    if request.method == 'GET':
        return episode_info
    if request.method == 'POST':
        ''' Trata las votaciones '''
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
        if request.is_ajax():
            votes = Vote.objects.get_score(link)
            return HttpResponse(simplejson.dumps(votes), mimetype='application/json')
        episode_info.update({
            'message': 'Vote recorded',
        })
        return episode_info


def list_user_recommendation(request):
    return "TODO: listar las recomendaciones para el usuario"


@render_to('serie/serie_list.html')
def get_serie_list(request, slug_name=None, query_type=None):
    ''' Listado de series con paginacion, genero y cadena '''
    genre_list = Genre.objects.order_by('name').all()
    network_list = Network.objects.order_by('name').all()
    initial_query = {
            'genre_list': genre_list,
            'network_list': network_list,
        }
    serie_list = Serie.objects.select_related('poster').order_by('name')
    if query_type == 'genre' and slug_name:
        genre = get_object_or_404(Genre, slug_name=slug_name)
        serie_list = Serie.objects.select_related('poster').filter(genres=genre.id).order_by('name')
        initial_query.update({'genre': genre,})
    elif query_type == 'network' and slug_name:
        network = get_object_or_404(Network, slug_name=slug_name)
        serie_list = Serie.objects.select_related('poster').filter(network=network.id).order_by('name')
        initial_query.update({'network': network,})
    paginator = NamePaginator(
        serie_list,
        on="name",
        per_page = 10
    )
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    initial_query.update({'page': page,})
    return initial_query 


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
    # Si es para editar, devolvemos la instancia del link ya existente ;)
    # Esto es solo para presentar el form, para el post viene mas adelante...
    if request.method == 'GET' and request.GET.get('edit') and request.GET.get('linkid'):
        linkid = request.GET.get('linkid')
        link = Link.objects.get(pk=linkid)
        if request.user.username == link.user:
            form = LinkForm(instance=link) 
            link_info.update({ 'form': form, 'edit': 'yes', 'link': link, })
            return link_info
    # Este es el formulario inicial, si el request.method es GET
    # pre-populamos con el episodio, que eso ya lo tenemos de la URL
    if request.method == 'GET':
        form = LinkForm(initial={ 'episode':episode }) 
        link_info.update({ 'form': form, })
        return link_info
    # Cuando se envia el formulario...
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
            if not form.cleaned_data['url'].startswith('http://'):  # TODO: agregar magnet/ed2k, otros URIs
                link_info.update({ 'message': 'URL Invalida',})
                return link_info
            # Audio Lang, Subtitle y Episode hay que pasarlos como instancias
            # Episode ya lo tenemos, vamos a buscar audio_lang
            lang = Languages.objects.get(pk=data['audio_lang'])
            # si en el POST encontramos el edit, pues esta editando :S
            if request.GET.get('edit'):
                print "editando un link existente"
                # capturamos el link q esta editando y agregamos las modificaciones
                link = Link.objects.get(pk=request.GET.get('linkid'))
                link.url=form.cleaned_data['url']
                link.audio_lang=lang
                link.user=form.cleaned_data['user']
                link.episode=episode
                link.pub_date=form.cleaned_data['pub_date']
                if form.cleaned_data['subtitle']:
                    subt = Languages.objects.get(pk=data['subtitle'])
                    link.subtitle = subt
                link.save()
                link_info.update({ 'message': 'Gracias',})
                return link_info
            # sino, es un link nuevo
            else:
                link = Link(
                    url=form.cleaned_data['url'],
                    audio_lang=lang,
                    user=form.cleaned_data['user'],
                    episode=episode,
                    pub_date=form.cleaned_data['pub_date'],
                )
                if form.cleaned_data['subtitle']:
                    subt = Languages.objects.get(pk=data['subtitle'])
                    link.subtitle = subt
                link.save()
                link_info.update({ 'message': 'Gracias',})
                return link_info
        else:
            link_info.update({ 'message': 'Error',})
            return link_info



@render_to('serie/sneak_links.html')
def sneak_links(request):
    ''' Ultimos enlaces agregados '''
    last_links = Link.objects.order_by('-pub_date')[:30]
    return { 'last_links' : last_links }


def serie_lookup(request, serie_id):
    ''' JQuery PopUp en las imagenes '''
    serie = Serie.objects.get(id=serie_id)
    result = '<div><div class="left"><h3>' + serie.name + '</h3>'
    genres = serie.genres.all()
    genre_list = ''
    for genre in genres: genre_list += genre.name + ', '
    result += '<b>Genero</b>: ' + genre_list[:-2] + '<br />'
    result += '<b>Cadena</b>: ' + serie.network.name + '<br /><br /></div>'
    rating = serie.rating.get_rating()
    if rating > 3: background = 'positive_bg'
    elif rating > 2: background = 'neutral_bg'
    elif rating > 0: background = 'negative_bg'
    elif rating == 0: background = 'no_bg'
    result += '<div class="right"> <div class="center rating_num ' + background + ' ">' 
    result += str(rating) + '<div class="mt_3">de 5</div></div></div></div>'
    result += '<p style="margin-top:7em;">' + serie.description[:300] + '... </p>'
    return HttpResponse(result)


def season_lookup(request, serie_slug, season):
    serie = Serie.objects.get(slug_name=serie_slug)
    season = Season.objects.get(serie=serie, season=season)
    episode_list = season.episodes.all().order_by('episode')
    episode_string = '<div id="episode_list"><ul>\n'
    for episode in episode_list:
        episode_string += '<li><a href="%s"><strong>%s</strong> - %s </a></li>\n' % ( episode.get_absolute_url(), episode.season_episode(), episode.title )
    episode_string += '</ul></div>'
    return HttpResponse(episode_string)


@render_to('serie/actors_lookup.html')
def actors_lookup(request, serie_slug):
    serie = Serie.objects.get(slug_name=serie_slug)
    roles = Role.objects.select_related('actor', 'serie', 'actor__poster').filter(serie = serie)
    return { 'roles': roles }

