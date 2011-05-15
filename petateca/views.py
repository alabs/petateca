from serie.models import Serie, Episode, Link
from decorators import render_to
from invitation.models import InvitationKey

from serie.models import Serie, Episode, Link
from voting.models import Vote
from django.contrib.auth.models import User
from djangoratings.models import Vote as Rating

@render_to('index.html')
def index(request):
    ''' Para la home '''
    serie_list = Serie.objects.order_by('rating_score').reverse().select_related('poster')[:5] 
    if request.user.is_authenticated():
        remaining_invitations = abs(InvitationKey.objects.remaining_invitations_for_user(request.user))
    else:
        remaining_invitations = 'anonymous'
    index_response = {
                'series': serie_list,
                'remaining_invitations': remaining_invitations,
         }
    # Le damos una cookie que queramos, luego comprobamos que este
    # para enviar los mensajes con jgrowl
    if request.session.get('logo_mess', False):
        return index_response
    else:
        request.session['logo_mess'] = True
        logo_message = 1
        index_response.update({
                'logo_message': logo_message,
         })
        return index_response

@render_to('statistics.html')
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
