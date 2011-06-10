from django.conf.urls.defaults import *
from django.conf import settings

from django.views.generic.simple import redirect_to

from django.contrib import admin
admin.autodiscover()

from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
    (r'^$', 'views.index'),
    # estadistcas
    (r'^stats/$', 'views.statistics'),

    (r'^sentry/', include('sentry.urls')),

    (r'^serie/', include('serie.urls.obj')),
    (r'^series/', include('serie.urls.entity')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    url(r'^api/$', redirect_to, { 'url': '/api/v1' }, name='api'),
    (r'^api/v1/', include('api_v1.urls')),
    (r'^api/v2/', include('api_v2.urls')),

    (r'^search/', include('search.urls')),

    (r'^i18n/', include('django.conf.urls.i18n')),

    (r'^favicon\.ico$', redirect_to, {'url': '/static/images/favicon.ico'}),
    url(r'^opensearch.xml/$', direct_to_template, \
        {'template': 'opensearch.xml'}, name="opensearch"),
    url(r'^faq/$', direct_to_template, \
        {'template': 'faq.html'}, name="faq"),
    url(r'^aviso-legal/$', direct_to_template, \
        {'template': 'aviso-legal.html'}, name="aviso-legal"),
    url(r'^politica-privacidad/$', direct_to_template, 
        {'template': 'politica-privacidad.html'}, name="politica-privacidad"),

    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^accounts/', include('userdata.urls')),
    url(r'^user/(?P<user_name>[-\w]+)$', 'userdata.views.get_user_public_profile', name='user_profile'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^rosetta/', include('rosetta.urls')),
    )
