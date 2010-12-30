from django.conf.urls.defaults import patterns, url
from serie.models import Link
from voting.views import vote_on_object

urlpatterns = patterns('liberweb.serie.views',
    url(r'^(?P<serie_slug>[-\w]+)/$', 'get_serie', name='get_serie'),
    url(r'^(?P<serie_slug>[-\w]+)/season/(?P<season>\d+)/$', 'get_season', name='get_season'),
    url(r'^(?P<serie_slug>[-\w]+)/episodes/S(?P<season>\d+)E(?P<episode>\d+)/$', 'get_episode', name='get_episode'),

    (r'^(?P<serie_slug>[-\w]+)/episodes/$', 'get_episodes'),

 #   (r'^(?P<serie_slug>[-\w]+)/episodes/S(?P<season>\d+)E(?P<episode>\d+)/link/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/$',
 #       vote_on_object, {
 #           'model': Link,
 #           'template_object_name': 'link',
 #           'allow_xmlhttprequest': True,
 #       }
 #   ),


)
