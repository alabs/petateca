from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from haystack.views import SearchView, search_view_factory
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'liberweb.views.index'),

    (r'^serie/', include('liberweb.serie.urls.obj')),
    (r'^series/', include('liberweb.serie.urls.entity')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^blog/', include('liberweb.blog.urls')),


    (r'^search/$', search_view_factory(
        view_class=SearchView,
        searchqueryset=SearchQuerySet(),
        form_class=ModelSearchForm
    )),

    (r'^i18n/', include('django.conf.urls.i18n')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^rosetta/', include('rosetta.urls')),
    )
