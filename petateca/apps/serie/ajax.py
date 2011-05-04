from serie.models import Serie, Episode, Actor, Role, Season, Network, Genre, Link, Languages, LinkSeason
from django.contrib import messages
from serie.forms import LinkForm, LinkSeasonForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils import simplejson
from voting.models import Vote
from django.http import HttpResponse
from decorators import render_to
from datetime import datetime

@render_to('serie/ajax_serie.html')
def serie_lookup(request, serie_id):
    ''' JQuery PopUp en las imagenes '''
    serie = get_object_or_404(Serie, id=serie_id)
    genres = serie.genres.all()
    return { 'serie' : serie, 'genres': genres }


@render_to('serie/ajax_season.html')
def season_lookup(request, serie_id, season):
    serie = get_object_or_404(Serie, id=serie_id)
    season = get_object_or_404(Season, serie=serie, season=season)
    episode_list = season.episodes.all().order_by('episode')
    return { 
        'season': season,
        'episode_list' : episode_list,
    }


@render_to('serie/ajax_links_season.html')
def links_season_lookup(request, serie_id, season):
    serie = get_object_or_404(Serie, id=serie_id)
    season = get_object_or_404(Season, serie=serie, season=season)
    link_list = season.links.all()
    return { 
        'season': season,
        'link_list': link_list,
    }


@render_to('serie/ajax_episodes.html')
def links_episode_lookup(request, serie_id, season, episode):
    serie = get_object_or_404(Serie, id=serie_id)
    season = get_object_or_404(Season, serie=serie, season=season)
    episode = get_object_or_404(Episode, episode=episode, season=season)
    link_list = episode.links.all()
    return { 
        'season': season,
        'link_list': link_list,
    }


@render_to('serie/ajax_espoiler.html')
def espoiler_lookup(request, serie_id, season, episode):
    serie = get_object_or_404(Serie, id=serie_id)
    season = Season.objects.get(serie=serie, season=season)
    episode = get_object_or_404(Episode, episode=episode, season=season)
    return {
        'serie': serie,
        'episode': episode, 
    }


@login_required
def vote_link(request):
    if request.method == 'POST':
        ''' Trata las votaciones '''
        user = User.objects.get(username=request.user)
        link = Link.objects.get(id=request.POST['linkid'])
        if request.POST['vote'] == 'upvote':
            Vote.objects.record_vote(link, user, +1)
        elif request.POST['vote'] == 'downvote':
            Vote.objects.record_vote(link, user, -1)
        if request.is_ajax():
            votes = Vote.objects.get_score(link)
            return HttpResponse(simplejson.dumps(votes), mimetype='application/json')

@login_required
def vote_link_season(request):
    if request.method == 'POST':
        ''' Trata las votaciones '''
        user = User.objects.get(username=request.user)
        link = LinkSeason.objects.get(id=request.POST['linkid'])
        if request.POST['vote'] == 'upvote':
            Vote.objects.record_vote(link, user, +1)
        elif request.POST['vote'] == 'downvote':
            Vote.objects.record_vote(link, user, -1)
        if request.is_ajax():
            votes = Vote.objects.get_score(link)
            return HttpResponse(simplejson.dumps(votes), mimetype='application/json')


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
    genre = get_object_or_404(Genre, slug_name = genre_slug)
    return { 'series_list': genre.series.all() }


@render_to('serie/generic_list.html')
def ajax_network(request, network_slug):
    network = get_object_or_404(Network, slug_name = network_slug)
    return { 'series_list': network.series.all() }



@login_required
@render_to('serie/ajax_add_link.html')
def ajax_add_link(request, episode_id):
    ''' 
    Formulario que agrega/edita links en AJAX
    ''' 
    episode = get_object_or_404(
        Episode,
        id=episode_id
    )
    link_info = {
        'serie': episode.season.serie,
        'episode': episode,
        'season': episode.season,
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
        form = LinkForm(initial={ 'episode':episode, 'url':'http://', }) 
        link_info.update({ 'form': form, })
        return link_info
    # Cuando se envia el formulario...
    if request.method == 'POST':
        # Capturamos lo que nos pasa, agregamos el episode
        # fecha de publicacion y usuario que hace la peticion
        user = User.objects.get(username=request.user.username)
        now = datetime.now()
        data = {
            'url': request.POST['url'], 
            'audio_lang': request.POST['audio_lang'], 
            'subtitle': request.POST['subtitle'], 
            'user': user,
            'episode': episode.pk, 
            'pub_date': now,
        } 
        form = LinkForm(data)
        link_info.update({'form': form})
        if form.is_valid():
            # Comprobamos que el form sea correcta, lo procesamos
            if not form.cleaned_data['url'].startswith('http://'):  # TODO: agregar magnet/ed2k, otros URIs
                messages.error(request, 'URL invalida')
                return { 'mensaje' : 'Invalida' }
            # Audio Lang, Subtitle y Episode hay que pasarlos como instancias
            # Episode ya lo tenemos, vamos a buscar audio_lang
            lang = Languages.objects.get(pk=data['audio_lang'])
            # si en el POST encontramos el edit, pues esta editando :S
            if request.GET.get('edit'):
                # capturamos el link q esta editando y agregamos las modificaciones
                link = Link.objects.get(pk=request.GET.get('linkid'))
                link.url=form.cleaned_data['url']
                link.audio_lang=lang
                link.user=user
                link.episode=episode
                link.pub_date=now
                if form.cleaned_data['subtitle']:
                    subt = Languages.objects.get(pk=data['subtitle'])
                    link.subtitle = subt
                # El aguila esta en el nido
                link.save()
               # messages.info(request, 'Gracias')
                return HttpResponse(simplejson.dumps({'mensaje': 'Gracias'}), mimetype='application/json')
            # sino, es un link nuevo
            else:
                link = Link(
                    url=form.cleaned_data['url'],
                    audio_lang=lang,
                    user=user,
                    episode=episode,
                    pub_date=now,
                )
                if form.cleaned_data['subtitle']:
                    subt = Languages.objects.get(pk=data['subtitle'])
                    link.subtitle = subt
                link.save()
                #messages.info(request, 'Gracias')
                return HttpResponse(simplejson.dumps({'mensaje': 'Gracias'}), mimetype='application/json')
        else:
            messages.error(request, 'Error')
            return link_info



@login_required
@render_to('serie/ajax_add_link_season.html')
def ajax_add_link_season(request, season_id):
    ''' 
    Formulario que agrega/edita links en AJAX para las Temporadas
    ''' 
    season = get_object_or_404(
        Season,
        id=season_id
    )
    link_info = {
        'serie': season.serie,
        'season': season,
    }
    # Si es para editar, devolvemos la instancia del link ya existente ;)
    # Esto es solo para presentar el form, para el post viene mas adelante...
    if request.method == 'GET' and request.GET.get('edit') and request.GET.get('linkid'):
        linkid = request.GET.get('linkid')
        link = LinkSeason.objects.get(pk=linkid)
        if request.user.username == link.user:
            form = LinkSeasonForm(instance=link) 
            link_info.update({ 'form': form, 'edit': 'yes', 'link': link, })
            return link_info
    # Este es el formulario inicial, si el request.method es GET
    # pre-populamos con el episodio, que eso ya lo tenemos de la URL
    if request.method == 'GET':
        form = LinkSeasonForm(initial={ 'season':season, 'url':'http://', }) 
        link_info.update({ 'form': form, })
        return link_info
    # Cuando se envia el formulario...
    if request.method == 'POST':
        # Capturamos lo que nos pasa, agregamos la temporada
        # fecha de publicacion y usuario que hace la peticion
        user = User.objects.get(username=request.user.username)
        now = datetime.now()
        data = {
            'url': request.POST['url'], 
            'audio_lang': request.POST['audio_lang'], 
            'subtitle': request.POST['subtitle'], 
            'user': user,
            'season': season.pk, 
            'pub_date': now,
        } 
        form = LinkSeasonForm(data)
        link_info.update({'form': form})
        if form.is_valid():
            # Comprobamos que el form sea correcta, lo procesamos
            if not form.cleaned_data['url'].startswith('http://'):  # TODO: agregar magnet/ed2k, otros URIs
                messages.error(request, 'URL invalida')
                return { 'mensaje' : 'Invalida' }
            # Audio Lang, Subtitle y Episode hay que pasarlos como instancias
            # Episode ya lo tenemos, vamos a buscar audio_lang
            lang = Languages.objects.get(pk=data['audio_lang'])
            # si en el POST encontramos el edit, pues esta editando :S
            if request.GET.get('edit'):
                # capturamos el link q esta editando y agregamos las modificaciones
                link = LinkSeason.objects.get(pk=request.GET.get('linkid'))
                link.url=form.cleaned_data['url']
                link.audio_lang=lang
                link.user=user
                link.season=season
                link.pub_date=now
                if form.cleaned_data['subtitle']:
                    subt = Languages.objects.get(pk=data['subtitle'])
                    link.subtitle = subt
                # El aguila esta en el nido
                link.save()
               # messages.info(request, 'Gracias')
                return HttpResponse(simplejson.dumps({'mensaje': 'Gracias'}), mimetype='application/json')
            # sino, es un link nuevo
            else:
                link = LinkSeason(
                    url=form.cleaned_data['url'],
                    audio_lang=lang,
                    user=user,
                    season=season,
                    pub_date=now,
                )
                if form.cleaned_data['subtitle']:
                    subt = Languages.objects.get(pk=data['subtitle'])
                    link.subtitle = subt
                link.save()
                #messages.info(request, 'Gracias')
                return HttpResponse(simplejson.dumps({'mensaje': 'Gracias'}), mimetype='application/json')
        else:
            messages.error(request, 'Error')
            return link_info


