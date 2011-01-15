from liberweb.serie.models import Serie, Episode, Link
from liberweb.blog.models import Post
from django.contrib import messages
from liberweb.decorators import render_to
from liberweb.settings import SITE_NAME

@render_to('index.html')
def index(request):
    post_list = Post.objects.all().order_by('-date')[:3]
    post_list_2 = Post.objects.all().order_by('-date')[3:6]
    serie_list = Serie.objects.order_by('?')[:5]  # ?=random
    count_link = Link.objects.all().count()
    count_episode = Episode.objects.all().count()
    count_serie = Serie.objects.all().count()
    index_response = {
                'posts': post_list,
                'posts2': post_list_2,
                'series': serie_list,
                'title': SITE_NAME,
                'count_link': count_link,
                'count_episode': count_episode,
                'count_serie': count_serie,
         }
    if request.session.get('visited', False):
        return index_response
    else:
        request.session['visited'] = True
        initial_message = 1
        return index_response.update({
                'initial_message': initial_message,
         })
