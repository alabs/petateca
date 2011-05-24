from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError

from djangoratings.views import AddRatingView
from decorators import render_to

from serie.forms import SerieForm, ImageSerieForm
from serie.models import Serie, Season, Link, ImageSerie



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
    # Entregamos el formulario
    if request.method == 'GET':
        if serie_slug:
        # Si hay una serie no es add, es edit, ergo devolvemos la instancia
            serie = Serie.objects.get(slug_name=serie_slug)
            form_serie = SerieForm(instance=serie)
            img_form = ImageSerieForm()
            return {
                    'form': form_serie,
                    'serie': serie,
                    'img_form': img_form,
                }
        else:
            # Agregar una serie, este es el formulario limpio
            form_serie = SerieForm()
            img_form = ImageSerieForm()
            return {
                'form': form_serie,
                'img_form': img_form,
            }

    # Respuesta, nos llega el formulario
    if request.method == 'POST':
        # TODO: preparamos los actores/roles
        serie_post_clean = request.POST.copy()
        serie_post_clean['slug_name'] = slugify(request.POST['name_es'])
        # Le pasamos a modeltranslation los campos por defecto en spanish
        serie_post_clean['name'] = request.POST['name_es']
        serie_post_clean['description'] = request.POST['description_es']
        # Si hay una serie no es add, es edit, ergo tratamos la instancia
        if serie_slug:
            serie = Serie.objects.get(slug_name=serie_slug)
            # para que no joda el poster ya existente
            try:
                serie_post_clean['poster'] = serie.poster.id
            except:
                pass
            form_serie = SerieForm(serie_post_clean, instance=serie)
            img_form = ImageSerieForm()
        else:
            form_serie = SerieForm(serie_post_clean)
            img_form = ImageSerieForm()
        if form_serie.is_valid():
            if not serie_slug:
                try:
                    # Comprobamos que no exista ya una serie con ese nombre
                    name_es = form_serie.data['name_es']
                    name_en = form_serie.data['name_en']
                    serie = Serie.objects.get(
                            Q(name_es=name_es)|
                            Q(name_en=name_en)
                        )
                except IntegrityError:
                    return {
                        'message': 'Duplicada',
                        'form': form_serie,
                        'img_form': img_form,
                    }
            form_serie.save()
            # Si existe FILES es que nos envian una imagen para la serie
            if request.FILES:
                img_serie = ImageSerie()
                img_serie.title = serie_slug
                img_serie.src = request.FILES['src']
                img_serie.is_poster = True
                img_serie.serie = serie
                img_serie.save()
            # TODO: tratamiento de los actores
            final_url = reverse('serie.views.get_serie', kwargs={
                'serie_slug': form_serie.cleaned_data['slug_name']
            })
            # Redireccionamos a la ficha de la serie
            return HttpResponseRedirect(final_url)
        else:
            # uoops -- excepciones
            return {
                'message': form_serie.errors,
                'message2': img_form.errors,
                'form': form_serie,
                'img_form': img_form,
            }
