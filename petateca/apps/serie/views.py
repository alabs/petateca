from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError

from djangoratings.views import AddRatingView
from decorators import render_to

from serie.forms import SerieForm
from serie.models import Serie, Season, Link, Genre



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
@render_to('serie/add_or_edit_serie.html')
def add_or_edit_serie(request, serie_slug=None):
    '''
    Formulario que agrega/edita series
    '''
    if request.method == 'POST':
        if request.POST['finished'] == 'on': 
            serie_finished = True
        # TODO: preparamos los actores/roles
        # Convertimos los generos en una lista, separando el primero de los otros
        genres = request.POST['genres_raw']
        if ',' in genres: 
            genre_split = genres.split(',')
            genre = genre_split[0]
            all_genres = genre_split
        # TODO: posters
        serie_post_clean = request.POST.copy()
        serie_post_clean['slug_name'] = slugify(request.POST['name_es'])
        serie_post_clean['name'] = request.POST['name_en']
        serie_post_clean['description'] = request.POST['description_en']
        serie_post_clean['finished'] = serie_finished
        # pasamos el primer genre a taves de POST ...
        serie_post_clean['genres'] = genre
        # Si hay una serie no es add, es edit, ergo tratamos la instancia
        if serie_slug:
            serie = Serie.objects.get(slug_name=serie_slug)
            form_serie = SerieForm(serie_post_clean, instance=serie)
        else:
            form_serie = SerieForm(serie_post_clean)
        if form_serie.is_valid():
            try:
                form_serie.save()
                slug = form_serie.data['slug_name']
                s = Serie.objects.get(slug_name=slug)
                # ... y ahora si tratamos toods los generos
                s.genres.clear()
                for g in all_genres:
                    s.genres.add(Genre.objects.get(id=g))
                # TODO: tratamiento de los actores
                final_url = reverse('serie.views.get_serie', kwargs={
                    'serie_slug': slug
                })
                if serie:
                    result = 'Updated'
                else:
                    result = 'Created'
                return HttpResponse(
                    simplejson.dumps({ 'result': result, 'redirect': final_url }),
                    mimetype='application/json'
                )
                #return HttpResponseRedirect(final_url)
            except IntegrityError:
                return HttpResponse(
                    simplejson.dumps({ 'result': 'Duplicated' }),
                    mimetype='application/json'
                )
        else:
            return HttpResponse(
                simplejson.dumps({ 'result': 'Error'} ), 
                mimetype='application/json'
            )
    # Si hay una serie no es add, es edit, ergo devolvemos la instancia
    if serie_slug:
        serie = Serie.objects.get(slug_name=serie_slug)
        form_serie = SerieForm(instance=serie)
        return {
                'form': form_serie,
                'serie': serie,
            }
    else:
        # Agregar una serie
        form_serie = SerieForm()
        return {
            'form': form_serie,
        }
