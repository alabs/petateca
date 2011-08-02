# pylint: disable-msg=W0401,W0614
from django.conf.urls.defaults import *

urlpatterns = patterns('book.views',
    url(r'^(?P<book_slug>[-\w]+)/$', 'get_book', name='get_book'),

 #   # Edition serie
 #   url(r'^(?P<serie_slug>[-\w]+)/edit/$', 'add_or_edit_serie', name="edit_serie"),

 #   # Adding season of a serie
 #   url(r'^(?P<serie_slug>[-\w]+)/add/$', 'add_season', name="add_season"),
)

urlpatterns += patterns('book.ajax', 
    # Rate
    url(r'^(?P<book_slug>[-\w]+)/rate/$', 'rating_book', name="rating_book"),

    # Favorite
    url(r'^(?P<book_slug>[-\w]+)/favorite/$', 'favorite_book', name="favorite_book"),
)
