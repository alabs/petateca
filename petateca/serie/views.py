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
from serie.models import Serie, Episode, Actor, Role, Season

from datetime import datetime
from lib.namepaginator import NamePaginator
from decorators import render_to


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
    # preparamos a los actores en un dict
#    actors = []
#    for actor in serie.actors.select_related().all():
#        a = {}
#        try:
#            a.update({ 'name': actor.name })
#            a.update({ 'url': actor.get_absolute_url() })
#            a.update({ 'image': actor.images.get().src })
#            for role in actor.role_set.all():
#                r = []
#                r.append(role.role)
#            a.update({ 'roles': r })
#            actors.append(a)
#        except:
#            pass
#    seasons = []
#    for season in serie.season.select_related().all().order_by('season'):
#        s = {}
#        s.update({ 'season': season.season })
#        s.update({ 'url': season.get_absolute_url() })
#        try:
#            season_img = season.images.all()[0].src
#        except:
#            try:
#                season_img = img_src
#            except: 
#                season_img = None
#        s.update({ 'image': season_img })
#        seasons.append(s)
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
    if request.method == 'POST' and request.is_ajax():
        if request.user.is_authenticated():
            if request.POST.has_key('favorite'):
                user = User.objects.get(username=request.user)
                serie.favorite_of.add(user.profile)
                return HttpResponse(simplejson.dumps('yes'), mimetype='application/json')
            elif request.POST.has_key('no-favorite'):
                user = User.objects.get(username=request.user)
                serie.favorite_of.remove(user.profile)
                return HttpResponse(simplejson.dumps('no'), mimetype='application/json')
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
            return HttpResponse(simplejson.dumps('no-user'), mimetype='application/json')


@render_to('serie/get_season.html')
def get_season(request, serie_slug, season):
    ''' Get season, returns episode_list
    also handles link voting (courtesy of django-voting) '''
    serie = Serie.objects.select_related().get(slug_name=serie_slug)
    season = serie.season.select_related().get(season=season)
    episode_list = season.episodes.select_related().order_by('episode')
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
        if request.is_ajax():
            votes = Vote.objects.get_score(link)
            return HttpResponse(simplejson.dumps(votes), mimetype='application/json')
        return season_info


@csrf_protect
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
        'link_list': episode.links.all(),
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
        if request.is_ajax():
            votes = Vote.objects.get_score(link)
            return HttpResponse(simplejson.dumps(votes), mimetype='application/json')
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
    imgs = actor.images.all()
    img_src = imgs[0].src if imgs else None
    return {
        'actor': actor,
        'title': actor.name,
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
    # Si es para editar, devolvemos la instancia del link ya existente ;)
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
        ##If request.user.username == link.user:
        ##    form = LinkForm(instance=link) 
        ##    link_info.update({ 'form': form, 'edit': 'yes', })
        ##    return link_info
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
    last_links = Link.objects.order_by('-pub_date')[:30]
    return { 'last_links' : last_links }

