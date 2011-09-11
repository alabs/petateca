# pylint: disable-msg=W0401,W0614
from django.conf.urls.defaults import *


urlpatterns = patterns('book.views',
    url(r'^add/$', 'add_or_edit_book', name="add_book"),
    (r'^add/author/?$', 'add_author'),
    (r'^add/category/?$', 'add_category'),
    url(r'^sneak/$', 'sneak_links', name='sneak_links_book'),
)

urlpatterns += patterns('book.ajax',
    url(r'^$', 'book_index', name='book_index'), 
    url(r'^lookup/letter/(?P<letter>[-\w]+)/$', 'book_index'),
    url(r'^lookup/category/(?P<category_slug>[-\w]+)/$', 'book_index'),
    url(r'^lookup/author/(?P<author_slug>[-\w]+)/$', 'book_index'),

    # -tratar votaciones de los links
    url(r'^links/vote/(?P<link_type>[-\w]+)/$', 'vote_link', name='vote_link'),

    # - agregar links de episodios y temporada
    url(r'^links/add/(?P<link_type>[-\w]+)/(?P<obj_id>\d+)/$', 'ajax_add_link', name='ajax_add_link_book'),

)
