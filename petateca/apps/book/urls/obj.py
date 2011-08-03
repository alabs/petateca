# pylint: disable-msg=W0401,W0614
from django.conf.urls.defaults import *

urlpatterns = patterns('book.views',
    # get a book
    url(r'^(?P<book_slug>[-\w]+)/$', 'get_book', name='get_book'),

    # book editing 
    url(r'^(?P<book_slug>[-\w]+)/edit/$', 'add_or_edit_book', name="edit_book"),
)

urlpatterns += patterns('book.ajax', 
    # Rate
    url(r'^(?P<book_slug>[-\w]+)/rate/$', 'rating_book', name="rating_book"),

    # Favorite
    url(r'^(?P<book_slug>[-\w]+)/favorite/$', 'favorite_book', name="favorite_book"),
)
