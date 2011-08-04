from core.decorators import render_to

from serie.models import Serie, Link
#from book.models import Book

from voting.models import Vote
from django.contrib.auth.models import User
from djangoratings.models import Vote as Rating

from avatar.models import Avatar

@render_to('core/index.html')
def index(request):
    ''' Para la home '''
    serie_list = Serie.objects.order_by('rating_score').reverse().select_related('poster')[:15] 
#    books_list = Book.objects.order_by('rating_score').reverse().select_related('poster')[:7] 
    index_response = { 
        'series': serie_list,
       # 'books': books_list, 
    }
    # Le damos una cookie que queramos, luego comprobamos que este
    # para enviar los mensajes con jgrowl
    if request.user.is_authenticated():
        avatars = Avatar.objects.filter(user__username=request.user.username)
        if not avatars:
            index_response.update({
                    'image_avatar': 'OK',
            })
    return index_response

@render_to('core/statistics.html')
def statistics(request):
    ''' Muestra estadisticas de los links, series, usuarios, etc '''
    count_links = Link.objects.count()
    count_series = Serie.objects.count()
    count_votes = Vote.objects.count()
    count_users = User.objects.count()
    count_ratings = Rating.objects.count()
    return {
        'count_links': count_links,
        'count_series': count_series,
        'count_votes': count_votes,
        'count_users': count_users,
        'count_ratings': count_ratings,
    }
