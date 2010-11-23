from django.conf.urls.defaults import *
# seems like wildcard MUST be there http://code.djangoproject.com/ticket/5350 
#from django.conf.urls.defaults import patterns, include
from django.views.generic.list_detail import object_list

from liberweb.serie.models import Serie

urlpatterns = patterns('liberweb.serie.views',
    #url(r'^$', object_list, {
    #    'queryset': Serie.objects.order_by('name').all(),
    #}, name="serie-index"),
    url(r'^$', 'serie_list', name="serie-index"),
    (r'^popular$', object_list, {
        'queryset': Serie.objects.order_by('-name').all(), #XXX: Bad order
    }),
    (r'^last$', object_list, {
        'queryset': Serie.objects.order_by('-name').all(), #XXX: Bad order
    }),
    (r'^favorite$', 'list_user_favorite'),
    (r'^recommended$', 'list_user_recommendation'),
)
