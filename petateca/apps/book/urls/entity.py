# pylint: disable-msg=W0401,W0614
from django.conf.urls.defaults import *
#from django.views.generic.list_detail import object_detail

#get_actor = {
#    'template_name': 'serie/get_actor.html',
#    'template_object_name': 'actor',
#    'queryset': Actor.objects.select_related('poster').all(),
#    'slug_field': 'slug_name',
#}


urlpatterns = patterns('book.views',
#    url(r'^actor/(?P<slug>[-\w]+)/$', object_detail, get_actor, name="get_actor"),
#    url(r'^sneak/$', 'sneak_links', name="sneak_links"),
##    url(r'^add/$', 'add_or_edit_serie', name="add_serie"),
#    (r'^recommended/$', 'list_user_recommendation'),
)

