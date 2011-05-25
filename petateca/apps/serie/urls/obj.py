# pylint: disable-msg=W0401,W0614
from django.conf.urls.defaults import *

urlpatterns = patterns('serie.views',
    url(r'^(?P<serie_slug>[-\w]+)/$', 'get_serie', name='get_serie'),
    url(r'^(?P<serie_slug>[-\w]+)/edit/$', 'add_or_edit_serie', name="edit_serie"),
    url(r'^(?P<serie_slug>[-\w]+)/add/$', 'add_season', name="add_season"),
)
