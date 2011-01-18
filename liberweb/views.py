from liberweb.serie.models import Serie, Episode, Link
from liberweb.blog.models import Post
from liberweb.decorators import render_to

@render_to('index.html')
def index(request):
    serie_list = Serie.objects.order_by('?')[:5]  # ?=random
    count_link = Link.objects.all().count()
    count_episode = Episode.objects.all().count()
    count_serie = Serie.objects.all().count()
    index_response = {
                'series': serie_list,
                'count_link': count_link,
                'count_episode': count_episode,
                'count_serie': count_serie,
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

