from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse

from core.decorators import render_to

from serie.models import Serie
from userdata.models import User

@render_to('registration/profile.html')
@login_required
def view_profile(request):
    ''' TODO: Para cambiar cosas del perfil ''' 
    user_profile = request.user.get_profile()
    return { 'profile': user_profile, } 


@render_to('userdata/public_profile.html')
def public_profile(request, user_name):
    ''' Perfil publico del usuario ''' 
    user = get_object_or_404(User, username=user_name)
    # for series marked as favorite
    favorite_series = Serie.objects.select_related("poster").filter(favorite_of=user)
    # comments for series
    serie = ContentType.objects.get(app_label='serie', name='serie')
    comments_series = user.comment_comments.filter(content_type=serie.id).order_by('-submit_date')[:10]
    return {
        'user': user,
        'favorite_series': favorite_series,
        'comments_serie': comments_series,
    }


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


@render_to('userdata/tracking.html')
def show_tracking(request):
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        serie = request.POST.get('serie_id')
        episode = user.profile.viewed_episodes.get(season__serie=serie)
        episodes = episode.get_next_5_episodes()
        return { 'episodes': episodes }
    else:
        return HttpResponseForbidden('Error en la peticion AJAX')
