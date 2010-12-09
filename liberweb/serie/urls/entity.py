from django.conf.urls.defaults import patterns, url
from django.views.generic.list_detail import object_list
from liberweb.serie.models import Serie, Actor, Genre, Network

urlpatterns = patterns('liberweb.serie.views',
    #url(r'^$', object_list, {
    #    'queryset': Serie.objects.order_by('name').all(),
    #}, name="serie-index"),
    url(r'^$', 'get_serie_list', name="serie-index"),
    (r'^popular$', object_list, {
        'queryset': Serie.objects.order_by('-name').all(), #XXX: Bad order
    }),
    (r'^last$', object_list, {
        'queryset': Serie.objects.order_by('-name').all(), #XXX: Bad order
    }),
    (r'^favorite$', 'list_user_favorite'),
    (r'^recommended$', 'list_user_recommendation'),

    url(r'^actors$', object_list, {
        'queryset': Actor.objects.order_by('name').all(),
        'paginate_by': 100,
    }, name="actor-serie-list"),
    url(r'^actor/(\d+)$', 'get_actor', name="get_actor"),

    url(r'^genres$', object_list, { 
        'queryset': Genre.objects.order_by('name').all(),
    }, name="genre-list"),
    url(r'^genre/(?P<id>\d+)$', 'get_genre', name="get_genre"),

    url(r'^networks$', object_list, { 
        'queryset': Network.objects.order_by('name').all(),
    }, name="network-list"),
    url(r'^network/(?P<id>\d+)$', 'get_network', name="get_network"),

)
