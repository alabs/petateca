from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from serie.models import Link, Serie
from userdata.forms import UserToInviteForm
from userdata.models import UserProfile, User, UserToInvite

from decorators import render_to
from djangoratings.models import Vote

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
    user = User.objects.get(username=user_name)
    profile = UserProfile.objects.get(user=user)
    # for series marked as favorite
    #favorite_series = profile.favorite_series.all()
    favorite_series = Serie.objects.select_related("poster").filter(favorite_of=user)
    # for django-ratings of Series
    #rated_series = user.votes.all()
    rated_series = Vote.objects.select_related("content_object").filter(user=user.id)
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
    blog = ContentType.objects.get(app_label='blog', name='post')
    comments_blog = user.comment_comments.filter(content_type=blog.id).order_by('-submit_date')[:10]
    # comments for series
    serie = ContentType.objects.get(app_label='serie', name='serie')
    comments_serie = user.comment_comments.filter(content_type=serie.id).order_by('-submit_date')[:10]
    return {
        'user': user,
        'favorite_series': favorite_series,
        'rated_series': rated_series,
        'voted_links': voted_links,
        'comments_blog': comments_blog,
        'comments_serie': comments_serie,
    }


@render_to('registration/invitation.html')
def request_invitation(request):
    ''' Para que los futuros usuarios puedan pedir invitaciones '''
    if request.method =='GET':
        form = UserToInviteForm()
    elif request.method == 'POST': 
        form = UserToInviteForm(request.POST)
        if form.is_valid(): 
            u = UserToInvite()
            u.mail = form.cleaned_data['mail']
            u.save()
            return HttpResponseRedirect('/accounts/invitation/thanks/') # Redirect after POST
    return { 'form' : form }
