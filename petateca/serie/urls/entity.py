# pylint: disable-msg=W0401,W0614
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from serie.models import Serie

urlpatterns = patterns('serie.views',
    # serie_list, genre y network van a una view distinta pero a la misma template
    url(r'^$', 'get_serie_list', name="serie-index"),
    url(r'^genre/(?P<slug_name>[-\w]+)$', 'get_genre', name="get_genre"),
    url(r'^network/(?P<slug_name>[-\w]+)$', 'get_network', name="get_network"),

    (r'^last$', object_list, {
        'queryset': Serie.objects.order_by('-name').all(), #XXX: Bad order
    }),
    (r'^recommended$', 'list_user_recommendation'),

    url(r'^popular$', 'list_popular', name='list-popular'), 

    url(r'^actor/(?P<slug_name>[-\w]+)$', 'get_actor', name="get_actor"),

    url(r'^sneak$', 'sneak_links', name="sneak_links"),
)
