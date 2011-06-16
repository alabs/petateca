from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from invitation.models import InvitationKey
from core.decorators import render_to

from serie.models import Serie
from userdata.forms import UserToInviteForm
from userdata.models import User, UserToInvite

@render_to('registration/profile.html')
@login_required
def view_profile(request):
    ''' TODO: Para cambiar cosas del perfil ''' 
    user_profile = request.user.get_profile()
    return { 'profile': user_profile, } 


@render_to('userdata/user_public_profile.html')
def get_user_public_profile(request, user_name):
    ''' Perfil publico del usuario ''' 
    user = get_object_or_404(User, username=user_name)
    if request.user == user:
        remaining_invitations = abs(InvitationKey.objects.remaining_invitations_for_user(request.user))
    else:
        remaining_invitations = None
    # for series marked as favorite
    favorite_series = Serie.objects.select_related("poster").filter(favorite_of=user)
    # comments for series
    serie = ContentType.objects.get(app_label='serie', name='serie')
    comments_series = user.comment_comments.filter(content_type=serie.id).order_by('-submit_date')[:10]
    return {
        'user': user,
        'favorite_series': favorite_series,
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


@render_to('userdata/activation_by_code.html')
def activate_by_code(request):
    if request.POST.get('activation_key'):
        activation_key = request.POST.get('activation_key')
        final_url = reverse('registration.views.activate', kwargs={
            'activation_key': activation_key
        })
        return HttpResponseRedirect(final_url)
    else: 
        return {'mensaje': 'Error'}
