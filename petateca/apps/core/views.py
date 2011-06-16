from core.decorators import render_to

from serie.models import Serie, Link
from voting.models import Vote
from django.contrib.auth.models import User
from djangoratings.models import Vote as Rating


@render_to('core/index.html')
def index(request):
    ''' Para la home '''
    serie_list = Serie.objects.order_by('rating_score').reverse().select_related('poster')[:7] 
    return { 'series': serie_list, }
    # Le damos una cookie que queramos, luego comprobamos que este
    # para enviar los mensajes con jgrowl
   # if request.session.get('logo_voting', False):
   #     return index_response
   # else:
   #     request.session['logo_voting'] = True
   #     logo_message = 1
   #     index_response.update({
   #             'logo_message': logo_message,
   #      })
   #     return index_response

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
