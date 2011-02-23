# pylint: disable-msg=W0401,W0614
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from serie.models import Serie, Actor

get_actor = {
    'template_name': 'serie/get_actor.html',
    'template_object_name': 'actor',
    'queryset': Actor.objects.select_related('poster').all(),
    'slug_field': 'slug_name',
}

# not working yet
list_popular = {
    'queryset': Serie.objects.order_by('-rating_score').all(),
    'template_name': 'serie/list_popular.html',
    'template_object_name': 'series',
}

urlpatterns = patterns('serie.views',
    url(r'^$', 'get_serie_list', name="serie-index"),
    url(r'^by/(?P<query_type>[-\w]+)/(?P<slug_name>[-\w]+)$', 'get_serie_list', name="get_by_type"),

    url(r'^actor/(?P<slug>[-\w]+)$', object_detail, get_actor, name="get_actor"),

    (r'^last$', object_list, {
        'queryset': Serie.objects.order_by('-name').all(), #XXX: Bad order
    }),
    (r'^recommended$', 'list_user_recommendation'),
    url(r'^popular$', 'list_popular', name='list-popular'), 
    #url(r'^popular$', object_list, list_popular, name='list-popular'), 

    url(r'^sneak$', 'sneak_links', name="sneak_links"),
    url(r'^lookup/(?P<serie_id>[-\w]+)$', 'serie_lookup'),

)
