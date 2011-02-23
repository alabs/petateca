# pylint: disable-msg=W0401,W0614
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from serie.models import Serie

urlpatterns = patterns('serie.views',
    url(r'^$', 'get_serie_list', name="serie-index"),
    url(r'^(?P<query_type>[-\w]+)/(?P<slug_name>[-\w]+)$', 'get_serie_list', name="get_by_type"),

    (r'^last$', object_list, {
        'queryset': Serie.objects.order_by('-name').all(), #XXX: Bad order
    }),
    (r'^recommended$', 'list_user_recommendation'),

    url(r'^popular$', 'list_popular', name='list-popular'), 

    url(r'^actor/(?P<slug_name>[-\w]+)$', 'get_actor', name="get_actor"),

    url(r'^sneak$', 'sneak_links', name="sneak_links"),

    url(r'^lookup/(?P<serie_id>[-\w]+)$', 'serie_lookup')
)
