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
    (r'^comments/', include('django.contrib.comments.urls')),
    url(r'^sneak$', 'sneak_links', name="sneak_links"),
    (r'^recommended$', 'list_user_recommendation'),
)

urlpatterns += patterns('serie.ajax',
    url(r'^lookup/serie/(?P<serie_id>[-\w]+)$', 'serie_lookup'),
    url(r'^lookup/serie/(?P<serie_id>[-\w]+)/season/(?P<season>\d+)$', 'season_lookup'),
    url(r'^lookup/actors/(?P<serie_slug>[-\w]+)$', 'actors_lookup'),

    # AJAX /series
    url(r'^lookup/letter/(?P<letter>[-\w]+)$', 'ajax_letter'),
    url(r'^lookup/genre/(?P<genre_slug>[-\w]+)$', 'ajax_genre'),
    url(r'^lookup/network/(?P<network_slug>[-\w]+)$', 'ajax_network'),

    # AJAX /serie/nombre
    url(r'^lookup/espoiler/(?P<serie_id>[-\w]+)/(?P<season>\d+)/(?P<episode>\d+)/$', 'espoiler_lookup', name='ajax_espoiler'),
    url(r'^lookup/vote/$', 'vote_link', name='vote_link'),
    url(r'^lookup/links/(?P<serie_id>[-\w]+)/(?P<season>\d+)/(?P<episode>\d+)/$', 'links_episode_lookup', name='ajax_links_episodes'),
    url(r'^lookup/links/(?P<serie_id>[-\w]+)/season/(?P<season>\d+)/$', 'links_season_lookup', name='ajax_links_season'),
    url(r'^lookup/add_link/(?P<episode_id>\d+)/$', 'ajax_add_link', name='ajax_add_link'),
)
