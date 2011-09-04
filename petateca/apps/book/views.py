from django.shortcuts import get_object_or_404
from core.decorators import render_to
from django.views.decorators.csrf import csrf_protect

from book.models import Book, ImageBook

#from django.utils import simplejson
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response

from django import forms

from book.forms import BookForm, ImageBookForm, CategoryForm, AuthorForm



@render_to('core/get_object.html')
@csrf_protect
def get_book(request, book_slug):
    ''' Request a book, returns images and links,
    also treats star-rating, courtesy of django-ratings'''
    book = get_object_or_404(
        Book.objects.select_related(), 
        slug_name=book_slug
    )
    # Vemos si el usuario tiene el libro como favorito
    try:
        book.favorite_book.get(user=request.user.profile)
        favorite_status = 'yes'
    except:
        favorite_status = 'no'
    try:
        score = int(book.rating.get_rating_for_user(request.user))
    except:
        score = None
    return {
            'object': book,
            'score': score,
            'favorite': favorite_status,
            'object_type': 'book',
        }


#def list_user_recommendation(request):
#    return "TODO: listar las recomendaciones para el usuario"
#
#
#@render_to('serie/sneak_links.html')
#def sneak_links(request):
#    ''' Ultimos enlaces agregados '''
#    last_links = Link.objects.order_by('-pub_date')[:30]
#    return {'last_links' : last_links}


@login_required
@render_to('book/add_or_edit_book.html')
def add_or_edit_book(request, book_slug=None):
    '''
    Formulario que agrega/edita books
    '''
    # Entregamos el formulario
    if request.method == 'GET':
        if book_slug:
        # Si hay una book no es add, es edit, ergo devolvemos la instancia
            book = Book.objects.get(slug_name=book_slug)
            form_book = BookForm(instance=book)
            img_form = ImageBookForm()
            return {
                    'form': form_book,
                    'book': book,
                    'img_form': img_form,
                }
        else:
            # Agregar una book, este es el formulario limpio
            form_book = BookForm()
            img_form = ImageBookForm()
            return {
                'form': form_book,
                'img_form': img_form,
            }
    # Respuesta, nos llega el formulario
    if request.method == 'POST':
        # TODO: preparamos los actores/roles
        book_post_clean = request.POST.copy()
        book_post_clean['slug_name'] = slugify(request.POST['name'])
        # Le pasamos a modeltranslation los campos por defecto en spanish
        book_post_clean['name'] = request.POST['name']
        book_post_clean['description'] = request.POST['description']
        # Si hay una book no es add, es edit, ergo tratamos la instancia
        if book_slug:
            book = Book.objects.get(name=request.POST['name'])
            # para que no joda el poster ya existente
            try:
                book_post_clean['poster'] = book.poster.id
            except:
                pass
            form_book = BookForm(book_post_clean, instance=book)
            img_form = ImageBookForm()
        else:
            form_book = BookForm(book_post_clean)
            img_form = ImageBookForm()
        if form_book.is_valid():
            if not book_slug:
                try:
                    # Comprobamos que no exista ya una book con ese nombre
                    name = form_book.data['name']
                    book = Book.objects.get(
                            Q(name=name)
                        )
                except IntegrityError:
                    return {
                        'message': 'Duplicada',
                        'form': form_book,
                        'img_form': img_form,
                    }
                except ObjectDoesNotExist:
                    pass
            book = form_book.save()
            #slug = form_book.cleaned_data['slug_name']
            # Si existe FILES es que nos envian una imagen para la book
            if request.FILES:
                img_book = ImageBook()
                img_book.title = form_book.cleaned_data['name']
                img_book.src = request.FILES['src']
                img_book.is_poster = True
                img_book.book = book
                img_book.save()
                book.poster = img_book
                book.save()
            final_url = reverse('book.views.get_book', kwargs={
                'book_slug': book.slug_name
            })
            # Redireccionamos a la ficha de la book
            return HttpResponseRedirect(final_url)
        else:
            # uoops -- excepciones
            return {
                'message': form_book.errors,
                'message2': img_form.errors,
                'form': form_book,
                'img_form': img_form,
            }


def handlePopAdd(request, addForm, field, action):
    if request.method == "POST":
        form = addForm(request.POST)
        if form.is_valid():
            try:
                newObject = form.save()
            except forms.ValidationError:
                newObject = None
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                    (escape(newObject._get_pk_val()), escape(newObject)))
    else:
        form = addForm()
    pageContext = {'form': form, 'field': field, 'action': action}
    return render_to_response("book/popadd.html", pageContext)


@login_required
def add_author(request):
    return handlePopAdd(request, AuthorForm, 'autor', 'author')


@login_required
def add_category(request):
    return handlePopAdd(request, CategoryForm, 'categoria', 'category')

