from serie.models import Serie, Episode, Link
from decorators import render_to
from invitation.models import InvitationKey

@render_to('index.html')
def index(request):
    serie_list = Serie.objects.order_by('-rating_score').select_related('poster')[:6] 
    if request.user.is_authenticated():
        remaining_invitations = abs(InvitationKey.objects.remaining_invitations_for_user(request.user))
    else:
        remaining_invitations = 'anonymous'
    index_response = {
                'series': serie_list,
                'remaining_invitations': remaining_invitations,
         }
    if request.session.get('visited', False):
        return index_response
    else:
        request.session['visited'] = True
        initial_message = 1
        index_response.update({
                'initial_message': initial_message,
         })
        return index_response

