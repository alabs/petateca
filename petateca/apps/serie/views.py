from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_protect

from djangoratings.views import AddRatingView
from voting.models import Vote

from serie.forms import LinkForm, LinkSeasonForm, SerieForm, EpisodeForm, RoleForm
from serie.models import Genre, Network, Link, Languages, LinkSeason
from serie.models import Serie, Episode, Actor, Role, Season, ImageSerie, ImageActor

from datetime import datetime
from decorators import render_to
from django.forms.models import inlineformset_factory


@render_to('serie/get_serie.html')
@csrf_protect
def get_serie(request, serie_slug):
    ''' Request a serie, returns images and episodes,
    also treats star-rating, courtesy of django-ratings'''
    serie = get_object_or_404(
        Serie.objects.select_related(), 
        slug_name=serie_slug
    )
    # Vemos si el usuario tiene la serie como favorita
    try:
        serie.favorite_of.get(user=request.user.profile)
        favorite_status = 'yes'
    except:
        favorite_status = 'no'
    try:
        score = int(serie.rating.get_rating_for_user(request.user))
    except:
        score = None
    # Si el metodo es GET devuelve serie_info asi nomas
    if request.method == 'GET':
        # Preparamos serie_info con la serie, titulo, imagenes, episodios...
        serie_info = {
            'serie': serie,
            'title': serie.name.title(),
            'season_list': Season.objects.select_related('poster', 'serie') \
                .filter(serie=serie).order_by('season'),
            'score': score,
            'favorite': favorite_status,
        }
        return serie_info
    # si es POST trata el favorito/rating:
    # Reescribir las VOTACIONES a AJAX!!
    if request.method == 'POST' and request.is_ajax():
        if request.user.is_authenticated():
            user = User.objects.get(username=request.user)
            # Si es favorito (corazon)
            if 'favorite' in request.POST:
                serie.favorite_of.add(user.profile)
                return HttpResponse(
                    simplejson.dumps('yes'), 
                    mimetype='application/json'
                )
            elif request.POST.has_key('no-favorite'):
                serie.favorite_of.remove(user.profile)
                return HttpResponse(
                    simplejson.dumps('no'),
                    mimetype='application/json'
                )
            # Si es rating de estrellas
            if 'rating' in request.POST:
                content_type = ContentType.objects.get(
                    app_label='serie', 
                    name='serie'
                )
                params = {
                    'content_type_id': content_type.id,
                    'object_id': serie.id,
                    'field_name': 'rating',  # campo en el modelo
                    'score': request.POST['rating'],
                }
                response = AddRatingView()(request, **params)
                return HttpResponse(
                    simplejson.dumps(response.content),
                    mimetype='application/json'
                )
        else:
            # El usuario no esta autenticado
            return HttpResponse(
                simplejson.dumps('no-user'),
                mimetype='application/json'
            )


def list_user_recommendation(request):
    return "TODO: listar las recomendaciones para el usuario"


@render_to('serie/sneak_links.html')
def sneak_links(request):
    ''' Ultimos enlaces agregados '''
    last_links = Link.objects.order_by('-pub_date')[:30]
    return {'last_links' : last_links}


@login_required
@render_to('serie/add_serie.html')
def add_serie(request, slug_serie=None):
    '''
    Formulario que agrega/edita series
    '''
    form_serie = SerieForm()
    if slug_serie:
        serie = Serie.objects.get(slug_name=slug_serie)
        form_serie = SerieForm(instance=serie)
        return {
                'form': form_serie,
                'serie': serie,
            }
    if request.method == 'POST':
        print request.POST
        serie_name = request.POST['name']
        serie_name_es = request.POST['name_es']
        serie_name_en = request.POST['name_en']
        serie_slug = slugify(request.POST['name_en'])
        serie_description = request.POST['description']
        print request.POST['genres']
        if request.POST['finished'] == 'on': 
            serie_finished = True
        # TODO: preparamos los actores/roles
        serie_post_clean = {
            'name': serie_name,
            'name_es': serie_name_es,
            'name_en': serie_name_en,
            'slug_name': serie_slug,
            'description': serie_description,
            'description_es': request.POST['description_es'],
            'description_en': request.POST['description_en'],
            'runtime': request.POST['runtime'],
            'finished': serie_finished,
            'genres': list(request.POST['genres']),
            'network': request.POST['network']
            }
        form_serie = SerieForm(serie_post_clean)

        if form_serie.is_valid():
            form_serie.save()
            # TODO: guardamos tambien los actores
            return HttpResponse(
                simplejson.dumps('OK'), 
                mimetype='application/json'
            )
        else:
            # TODO: guardamos tambien los actores
            return HttpResponse(
                simplejson.dumps('Error'), 
                mimetype='application/json'
            )
    return {
        'form': form_serie,
    }
