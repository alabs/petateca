from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from haystack.views import SearchView, search_view_factory
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet

from serie.feeds import RSSLatestLinksFeed, RSSBlogFeed, AtomLatestLinksFeed, AtomBlogFeed

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

    (r'^faq/$', 'django.views.generic.simple.direct_to_template', {'template': 'faq.html'}),

    #(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    url(r'^rss/blog/$', RSSBlogFeed(), name='rssblogfeed'),
    url(r'^rss/links/$', RSSLatestLinksFeed(), name='rsslinksfeed'),
    url(r'^atom/blog/$', AtomBlogFeed(), name='atomblogfeed'),
    url(r'^atom/links/$', AtomLatestLinksFeed(), name='atomlinksfeed'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^rosetta/', include('rosetta.urls')),
    )
