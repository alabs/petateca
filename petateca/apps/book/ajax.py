from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from djangoratings.views import InvalidRating
from django.utils import simplejson

from book import models as m

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
