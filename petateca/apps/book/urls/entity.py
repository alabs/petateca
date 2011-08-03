# pylint: disable-msg=W0401,W0614
from django.conf.urls.defaults import *


urlpatterns = patterns('book.views',
    url(r'^add/$', 'add_or_edit_book', name="add_book"),
    (r'^add/author/?$', 'add_author'),
    (r'^add/category/?$', 'add_category'),
)

urlpatterns += patterns('book.ajax',
    # -tratar votaciones de los links
    url(r'^links/vote/(?P<link_type>[-\w]+)/$', 'vote_link', name='vote_link'),

    # - agregar links de episodios y temporada
    url(r'^links/add/(?P<link_type>[-\w]+)/(?P<obj_id>\d+)/$', 'ajax_add_link', name='ajax_add_link_book'),

)
