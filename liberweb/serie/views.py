from liberweb.serie.models import Serie, Episode
from liberweb.blog.models import Post
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def serie_list(request):
    series_list = Serie.objects.order_by('name').all()
    # FIXME: Paginator should be separating by letter
    #        Yes, I know it isn't a django Paginator what we need but 
    #        'there, I fixed it': http://thereifixedit.failblog.org/
    paginator = Paginator(series_list, 25) # Show 25 series per page 

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        series = paginator.page(page)
    except (EmptyPage, InvalidPage):
        series = paginator.page(paginator.num_pages)

    return render_to_response('serie/serie_list.html', {
        'series': series,
    })

def get_serie(request, serie_slug):
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    # get() returned more than one
    # img = serie.images.get() 
    imgs = serie.images.filter(is_poster=True)
    img_src = imgs[0].src if imgs else None

    return render_to_response('serie/get_serie.html', {
        'serie': serie,
        'title': serie.name,
        'image': img_src,
    })

def get_episodes(request, serie_slug):
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    episodes = serie.episodes.all().order_by('season')
    return render_to_response('serie/get_episodes.html', {
        'serie': serie,
        'episode_list': episodes,
        'title': _("Episodes of %(name)s") % {"name": serie.name}, 
    })

def get_episode(request, serie_slug, season, episode):
    serie = get_object_or_404(Serie, slug_name=serie_slug)
    episode = get_object_or_404(Episode, serie=serie, season=season, episode=episode)
    return render_to_response('serie/get_episode.html', {
        'serie': serie, 
        'episode': episode, 
    })

def list_user_favorite(request):
    return "TODO"

def list_user_recommendation(request):
    return "TODO"

def index(request):
    post_list = Post.objects.all().order_by('-date')[:6]
    serie_list = Serie.objects.order_by('?')[:5] # ?=random
    return render_to_response('serie/index.html', { 
            'posts': post_list, 
            'series': serie_list,
     })
