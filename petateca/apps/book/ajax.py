from datetime import datetime 

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from djangoratings.views import InvalidRating
from django.utils import simplejson
from django.db.models import Q
from django.shortcuts import get_object_or_404

from core.decorators import render_to

from book import models as m
from book.forms import BookLinkForm

from voting.models import Vote

@login_required
def favorite_book(request, book_slug):
    ''' Tratamiento de favoritos (book) ''' 
    if request.method == 'POST' and request.is_ajax():
        book = m.Book.objects.get(slug_name=book_slug)
        user = User.objects.get(username=request.user)
        if request.POST['favorite'] == 'yes':
            book.favorite_book.add(user.profile)
            return HttpResponse(
                simplejson.dumps('yes'), 
                mimetype='application/json'
            )
        elif request.POST['favorite'] == 'no':
            book.favorite_book.remove(user.profile)
            return HttpResponse(
                simplejson.dumps('no'),
                mimetype='application/json'
            )
    else:
        return HttpResponseForbidden('Error en la peticion AJAX')


@login_required
def rating_book(request, book_slug):
    ''' Tratamiento de ratings para books '''
    if request.method == 'POST' and request.is_ajax():
        book = m.Book.objects.get(slug_name=book_slug)
        if request.POST['rating']:
            try:
                book.rating.add(
                    score=request.POST['rating'],
                    user=request.user,
                    ip_address=request.META['REMOTE_ADDR']
                )
                response = 'Ok'
            except InvalidRating:
                response = 'Error'
            return HttpResponse(
                simplejson.dumps(response),
                mimetype='application/json'
            )
    else:
        return HttpResponseForbidden('Error en la peticion AJAX')


@login_required
def vote_link(request, link_type):
    ''' Tratamiento de los votos de los enlaces '''
    if request.method == 'POST' and request.is_ajax():
        ''' Trata las votaciones '''
        user = User.objects.get(username=request.user)
        link = m.BookLink.objects.get(id=request.POST['linkid'])
        if request.POST['vote'] == 'upvote':
            Vote.objects.record_vote(link, user, +1)
        elif request.POST['vote'] == 'downvote':
            Vote.objects.record_vote(link, user, -1)
        votes = Vote.objects.get_score(link)
        return HttpResponse(simplejson.dumps(votes), mimetype='application/json')


@login_required
@render_to('book/ajax/add_link.html')
def ajax_add_link(request, link_type, obj_id):
    ''' 
    Formulario que agrega/edita links en AJAX
    ''' 
#    import pdb; pdb.set_trace()
    book = get_object_or_404( m.Book, id=obj_id )
    Form = BookLinkForm
    # Si es para editar, devolvemos la instancia del link ya existente ;)
    # Esto es solo para presentar el form, para el post viene mas adelante...
#    if request.method == 'GET' and request.GET.get('edit') and request.GET.get('linkid'):
#        linkid = request.GET.get('linkid')
#        if link_type == 'episode':
#            link = m.Link.objects.get(pk=linkid)
#        elif link_type == 'season':
#            link = m.SeasonLink.objects.get(pk=linkid)
#        if request.user.username == link.user:
#            form = Form(instance=link) 
#            link_info.update({ 'form': form, 'edit': 'yes', 'link': link, })
#            return link_info
    # Este es el formulario inicial, si el request.method es GET
    # pre-populamos con el episodio, que eso ya lo tenemos de la URL
    if request.method == 'GET':
        form = Form(initial={ 'url':'http://', }) 
        return { 'book': book, 'form': form }
    # Cuando se envia el formulario...
    if request.method == 'POST':
        # Capturamos lo que nos pasa, agregamos el episode
        # fecha de publicacion y usuario que hace la peticion
        user = User.objects.get(username=request.user.username)
        now = datetime.now()
        data = {
            'url': request.POST['url'], 
            'lang': request.POST['lang'], 
            'user': user,
            'pub_date': now,
            'book': book.pk,
        } 
        form = Form(data)
        if form.is_valid():
            url = form.cleaned_data['url']
            # Comprobamos que el form sea correcta, lo procesamos
            if not url.startswith('http://') and not url.startswith('https://'):  # TODO: agregar magnet/ed2k, otros URIs
                return { 'mensaje' : 'Invalida', 'book' : book }
            # Audio Lang, Subtitle y Episode hay que pasarlos como instancias
            # Episode ya lo tenemos, vamos a buscar audio_lang
            #lang = m.BookLanguages.objects.get(pk=form.cleaned_data['lang'])
            # si en el POST encontramos el edit, pues esta editando :S
            if request.GET.get('edit'):
                print "TODO"
                return HttpResponse(simplejson.dumps({'mensaje': 'Error'}), mimetype='application/json')
               # if link_type == 'episode':
               #     link = m.Link.objects.get(pk=request.GET.get('linkid'))
               # elif link_type == 'season':
               #     link = m.LinkSeason.objects.get(pk=request.GET.get('linkid'))
               # # capturamos el link q esta editando y agregamos las modificaciones
               # link.url=form.cleaned_data['url']
               # link.audio_lang=lang
               # link.user=user
               # link.episode=episode
               # link.pub_date=now
               # if form.cleaned_data['subtitle']:
               #     subt = m.Languages.objects.get(pk=data['subtitle'])
               #     link.subtitle = subt
               # try:
               #     # El aguila esta en el nido
               #     link.save()
               #    # messages.info(request, 'Gracias')
               #     return HttpResponse(simplejson.dumps({'mensaje': 'Gracias'}), mimetype='application/json')
               # except:
               #     return HttpResponse(simplejson.dumps({'mensaje': 'Error'}), mimetype='application/json')
            # sino, es un link nuevo
            else:
                link = m.BookLink(
                    url=form.cleaned_data['url'],
                    lang=form.cleaned_data['lang'],
                    book=book,
                   # user=user,
                    pub_date=now,
                )
                link.save()
                #messages.info(request, 'Gracias')
                return HttpResponse(
                    simplejson.dumps({
                        'mensaje': 'Gracias',
                        'type': 'book'
                    }), mimetype='application/json')
        else:
            if form.errors['url'] == [u'Ya existe Book link con este URL.']:
                return HttpResponse(simplejson.dumps({'mensaje': 'Link duplicado'}), mimetype='application/json')
            else: 
                return HttpResponse(simplejson.dumps(form.errors), mimetype='application/json')


def get_numbers():
    books = m.Book.objects.filter(name__startswith="0") | \
    m.Book.objects.filter(name__startswith="1") | \
    m.Book.objects.filter(name__startswith="2") | \
    m.Book.objects.filter(name__startswith="3") | \
    m.Book.objects.filter(name__startswith="4") | \
    m.Book.objects.filter(name__startswith="5") | \
    m.Book.objects.filter(name__startswith="6") | \
    m.Book.objects.filter(name__startswith="7") | \
    m.Book.objects.filter(name__startswith="8") | \
    m.Book.objects.filter(name__startswith="9") 
    return books


def book_index(request,
        template="core/object_list.html",
        page_template="core/generic_list.html",
        letter=False,
        category_slug=False,
        author_slug=False,
    ):
    ''' 
    Paginacion para letras / categorias / autores / books favoritas hecho con endless pagination
    '''
    # TODO: select_related en letra, genero y cadena
    if letter: 
        # Paginacion de letras 
        if letter == "0":
            query = get_numbers().order_by('name')
        else:
            query = m.Book.objects.filter(
                    Q(name__startswith=letter) |
                    Q(name__startswith=letter.lower())
                ).order_by('name')
    elif category_slug:
        # Paginacion de categorias 
        query = get_object_or_404(m.Category, slug_name = category_slug).books.order_by('name').all()
    elif author_slug:
        # Paginacion de autores
        query = get_object_or_404(m.Author, slug_name = author_slug).books.order_by('name').all()
    else:
        # Paginacion de libros ordenadas por favoritas
        query = m.Book.objects.select_related('poster').order_by('-rating_score').all()
    context = {
        'objects': query, 
        'page_template': page_template,
        'object_type': 'book',
        'pagination_per_page': 18,
    }
    if request.is_ajax():
        template = page_template
    return render_to_response(template, context,
        context_instance=RequestContext(request))
