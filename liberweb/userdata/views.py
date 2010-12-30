from liberweb.decorators import render_to
from django.contrib.auth.decorators import login_required

@render_to('registration/profile.html')
@login_required
def view_profile(request):
    user_profile = request.user.get_profile()
    return {
      'profile': user_profile,
    }
