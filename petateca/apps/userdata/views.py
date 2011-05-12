from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.forms import ValidationError
from django.shortcuts import get_object_or_404

from invitation.models import InvitationKey
from djangoratings.models import Vote
from decorators import render_to

from serie.models import Link, Serie
from userdata.forms import UserToInviteForm
from userdata.models import UserProfile, User, UserToInvite


@render_to('registration/profile.html')
@login_required
def view_profile(request):
    ''' TODO: Para cambiar cosas del perfil ''' 
    user_profile = request.user.get_profile()
    return {
      'profile': user_profile, } 

@render_to('userdata/user_public_profile.html')
def get_user_public_profile(request, user_name):
    ''' Perfil publico del usuario ''' 
    user = get_object_or_404(User, username=user_name)
    profile = UserProfile.objects.get(user=user)
    if request.user == user:
        remaining_invitations = abs(InvitationKey.objects.remaining_invitations_for_user(request.user))
    else:
        remaining_invitations = None
    # for series marked as favorite
    favorite_series = Serie.objects.select_related("poster").filter(favorite_of=user)
    # for django-voting of Links
    # ok, so don't look at this, it's a little hack
    # first we get the voted links in raw 
    all_voted_links = user.vote_set.values()[:5]
    # all_voted_links[0] looks like this {'vote': 1, 'user_id': 1, 'id': 1, 'object_id': 100, 'content_type_id': 24}
    # fuck
    voted_links = []
    for vote in all_voted_links: 
        list_vote = Link.objects.select_related("episode").get(id = vote['object_id']), (vote['vote'])
        voted_links.append(list_vote)
    # comments for posts of blog
    serie = ContentType.objects.get(app_label='serie', name='serie')
    comments_series = user.comment_comments.filter(content_type=serie.id).order_by('-submit_date')[:10]
    return {
        'user': user,
        'favorite_series': favorite_series,
        'voted_links': voted_links,
        'comments_serie': comments_series,
        'remaining_invitations': remaining_invitations,
    }


@render_to('invitation/request.html')
def request_invitation(request):
    ''' Para que los futuros usuarios puedan pedir invitaciones '''
    if request.method =='GET':
        form = UserToInviteForm()
    elif request.method == 'POST': 
        form = UserToInviteForm(request.POST)
        if form.is_valid(): 
            mail = form.cleaned_data['mail']
            user_registered = User.objects.filter(email = mail)
            if user_registered:
                return { 
                    'error_registered' : 'Ya existe un usuario con ese correo', 
                    'form' : form 
                } 
            else:
                u = UserToInvite()
                u.mail = mail
                u.save()
                return { 'invited_mail': u.mail, 'TEMPLATE': 'invitation/thanks.html' }
    return { 'form' : form }
