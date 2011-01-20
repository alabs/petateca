from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from liberweb.serie.models import Serie, Actor, Genre, Network

urlpatterns = patterns('liberweb.serie.views',
    # cada una va a una view distinta pero a la misma template
    url(r'^$', 'get_serie_list', name="serie-index"),
    url(r'^genre/(?P<slug_name>[-\w]+)$', 'get_genre', name="get_genre"),
    url(r'^network/(?P<slug_name>[-\w]+)$', 'get_network', name="get_network"),

    (r'^last$', object_list, {
        'queryset': Serie.objects.order_by('-name').all(), #XXX: Bad order
    }),
    (r'^recommended$', 'list_user_recommendation'),

    url(r'^popular$', 'list_popular', name='list-popular'), 
    url(r'^favorite$', 'list_user_favorite', name='user-favorite'),

    url(r'^actor/(?P<slug_name>[-\w]+)$', 'get_actor', name="get_actor"),
)
