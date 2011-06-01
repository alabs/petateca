# pylint: disable-msg=W0401,W0614
from django.conf.urls.defaults import *

urlpatterns = patterns('serie.views',
    url(r'^(?P<serie_slug>[-\w]+)/$', 'get_serie', name='get_serie'),

    # Edition serie
    url(r'^(?P<serie_slug>[-\w]+)/edit/$', 'add_or_edit_serie', name="edit_serie"),

    # Adding season of a serie
    url(r'^(?P<serie_slug>[-\w]+)/add/$', 'add_season', name="add_season"),
)

urlpatterns += patterns('serie.ajax', 
    # Rate
    url(r'^(?P<serie_slug>[-\w]+)/rate/$', 'rating_serie', name="rating_serie"),

    # Favorite
    url(r'^(?P<serie_slug>[-\w]+)/favorite/$', 'favorite_serie', name="favorite_serie"),
)
