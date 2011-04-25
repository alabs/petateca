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

serie_list = {
    'queryset': Serie.objects.select_related('poster').order_by('-rating_score').all()[:16],
    'template_name': 'serie/serie_list.html',
}

urlpatterns = patterns('serie.views',
    url(r'^$', object_list, serie_list, name='serie-index'), 

    url(r'^actor/(?P<slug>[-\w]+)$', object_detail, get_actor, name="get_actor"),

    (r'^last$', object_list, {
        'queryset': Serie.objects.order_by('-name').all(), #XXX: Bad order
    }),
    (r'^recommended$', 'list_user_recommendation'),

    url(r'^sneak$', 'sneak_links', name="sneak_links"),

    # AJAX
    url(r'^lookup/serie/(?P<serie_id>[-\w]+)$', 'serie_lookup'),
    url(r'^lookup/serie/(?P<serie_id>[-\w]/+)/(?P<season>[-\w]/+)$', 'season_lookup'),
    url(r'^lookup/actors/(?P<serie_slug>[-\w]+)$', 'actors_lookup'),
    url(r'^lookup/letter/(?P<letter>[-\w]+)$', 'ajax_letter'),
    url(r'^lookup/genre/(?P<genre_slug>[-\w]+)$', 'ajax_genre'),
    url(r'^lookup/network/(?P<network_slug>[-\w]+)$', 'ajax_network'),

)
