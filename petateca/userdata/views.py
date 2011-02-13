from decorators import render_to
from django.contrib.auth.decorators import login_required
from userdata.models import UserProfile, User
from django.contrib.contenttypes.models import ContentType
from serie.models import Link


@render_to('registration/profile.html')
@login_required
def view_profile(request):
    user_profile = request.user.get_profile()
    return {
      'profile': user_profile,
    }


@render_to('userdata/user_public_profile.html')
def get_user_public_profile(request, user_name):
    user = User.objects.get(username=user_name)
    profile = UserProfile.objects.get(user=user)
    # for series marked as favorite
    favorite_series = profile.favorite_series.all()
    # for django-ratings of Series
    rated_series = user.votes.all()
    # for django-voting of Links
    # ok, so don't look at this, it's a little hack
    # first we get the voted links in raw 
    all_voted_links = user.vote_set.values()
    # all_voted_links[0] looks like this {'vote': 1, 'user_id': 1, 'id': 1, 'object_id': 100, 'content_type_id': 24}
    # fuck
    # so, we prepare a dict with a tuple with the link instance and the vote value 
    voted_links = []
    for vote in all_voted_links: 
        list_vote = Link.objects.get(id = vote['object_id']), (vote['vote'])
        voted_links.append(list_vote)
    # comments for posts of blog
    blog = ContentType.objects.get(app_label='blog', name='post')
    comments_blog = user.comment_comments.filter(content_type=blog.id)
    # comments for series
    serie = ContentType.objects.get(app_label='serie', name='serie')
    comments_serie = user.comment_comments.filter(content_type=serie.id)
    return {
        'user': user,
        'series': favorite_series,
        'rated_series': rated_series,
        'voted_links': voted_links,
        'comments_blog': comments_blog,
        'comments_serie': comments_serie,
    }
