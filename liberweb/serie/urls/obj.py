from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list

from liberweb.serie.models import Serie

urlpatterns = patterns('liberweb.serie.views',
    (r'^(?P<serie_slug>[a-z0-9-]+)/$', 'get_serie'),
    (r'^(?P<serie_slug>[a-z0-9-]+)/episodes/$', 'get_episodes'),
    (r'^(?P<serie_slug>[a-z0-9-]+)/episodes/(?P<episode_slug>[a-z0-9-]+)/$', 'get_episode'),
)
