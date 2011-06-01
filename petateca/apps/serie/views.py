from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from decorators import render_to

from serie.forms import SerieForm, ImageSerieForm, SeasonForm
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
    return {
            'serie': serie,
            'season_list': Season.objects.filter(serie=serie).order_by('season'),
            'score': score,
            'favorite': favorite_status,
        }


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
                except ObjectDoesNotExist:
                    pass
            serie = form_serie.save()
            slug = form_serie.cleaned_data['slug_name']
            # Si existe FILES es que nos envian una imagen para la serie
            if request.FILES:
                img_serie = ImageSerie()
                img_serie.title = slug
                img_serie.src = request.FILES['src']
                img_serie.is_poster = True
                img_serie.serie = serie
                img_serie.save()
            # TODO: tratamiento de los actores
            final_url = reverse('serie.views.get_serie', kwargs={
                'serie_slug': slug
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


@login_required
@render_to('serie/add_season.html')
def add_season(request, serie_slug):
    serie = Serie.objects.get(slug_name=serie_slug)
    if request.method == 'GET':
        form_season = SeasonForm(initial={'serie': serie.id})
        return { 'form_season': form_season, 'serie': serie, }
    if request.method == 'POST':
        form_season = SeasonForm(request.POST)
        if form_season.is_valid():
                season, result = Season.objects.get_or_create(
                    season = form_season.cleaned_data['season'],
                    serie = serie
                )
                # if season doesn't exists
                if result == True:
                    season.save()
                    return HttpResponse(
                        simplejson.dumps({
                            'message': 'OK',
                            'redirect': serie.get_absolute_url(),
                            }), 
                        mimetype='application/json'
                    )
                # if exists, it's duplicated
                elif result == False:
                    return HttpResponse(
                        simplejson.dumps({'message': 'Duplicated'}), 
                        mimetype='application/json'
                    )
        # if not number
        else:
            return HttpResponse(
                simplejson.dumps({'message': 'Error'}), 
                mimetype='application/json'
            )
