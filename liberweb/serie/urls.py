from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list

from liberweb.serie.models import Serie

object_patterns = patterns('liberweb.serie.views',
    (r'^(?P<serie_slug>[a-z0-9-]+)/$', 'get_serie'),
    (r'^(?P<serie_slug>[a-z0-9-]+)/episodes/$', 'get_episodes'),
    (r'^(?P<serie_slug>[a-z0-9-]+)/episodes/(?P<episode_slug>[a-z0-9-]+)/$', 'get_episode'),
)

collection_patterns = patterns('liberweb.serie.views',
    url(r'^$', object_list, {
        'queryset': Serie.objects.order_by('name').all(),
    }, name="serie-index"),
    (r'^popular$', object_list, {
        'queryset': Serie.objects.order_by('-name').all(), #XXX: Bad order
    }),
    (r'^last$', object_list, {
        'queryset': Serie.objects.order_by('-name').all(), #XXX: Bad order
    }),
    (r'^favorite$', 'list_user_favorite'),
    (r'^recommended$', 'list_user_recommendation'),
)

urlpatterns = patterns('liberweb.serie.view',
    (r'^/', include(object_patterns)),
    (r'^s/', include(collection_patterns)),
)
