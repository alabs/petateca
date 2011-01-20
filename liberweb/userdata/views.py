from liberweb.decorators import render_to
from django.contrib.auth.decorators import login_required
from liberweb.userdata.models import UserProfile, User


@render_to('registration/profile.html')
@login_required
def view_profile(request):
    user_profile = request.user.get_profile()
    return {
      'profile': user_profile,
    }


@render_to('serie/list_user_favorite.html')
def get_series_favorite(request, user_name):
    user = User.objects.get(username=user_name)
    profile = UserProfile.objects.get(user=user)
    favorite_series = profile.favorite_series.all()
    return { 'series': favorite_series }

