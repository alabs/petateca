from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from haystack.views import SearchView, search_view_factory
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet

from serie.feeds import RSSLatestLinksFeed, RSSBlogFeed
from serie.feeds import AtomLatestLinksFeed, AtomBlogFeed

from django.views.generic.simple import redirect_to

from registration.forms import RegistrationFormUniqueEmail

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'liberweb.views.index'),

    (r'^serie/', include('liberweb.serie.urls.obj')),
    (r'^series/', include('liberweb.serie.urls.entity')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^blog/', include('liberweb.blog.urls')),

    (r'^search/lookup/$', 'liberweb.search.views.search_lookup'),

    (r'^search/$', search_view_factory(
        view_class=SearchView,
        searchqueryset=SearchQuerySet(),
        form_class=ModelSearchForm
    )),


    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^localeurl/', include('localeurl.urls')),

    url(r'^faq/$', 'django.views.generic.simple.direct_to_template',
        {'template': 'faq.html'},
        name="faq"
       ),

    url(r'^rss/blog/$', RSSBlogFeed(), name='rssblogfeed'),
    url(r'^rss/links/$', RSSLatestLinksFeed(), name='rsslinksfeed'),
    url(r'^atom/blog/$', AtomBlogFeed(), name='atomblogfeed'),
    url(r'^atom/links/$', AtomLatestLinksFeed(), name='atomlinksfeed'),


    (r'^accounts/profile/$', 'liberweb.userdata.views.view_profile'),

    #  url(r'^accounts/register/$', 'registration.views.register', {
    #      'backend': 'registration.backends.default.DefaultBackend',
    #      'form_class': RegistrationFormUniqueEmail,
    #  }, name='registration_register'),

    #  url(r'^accounts/login/$', 'registration.views.register', {
    #      'backend': 'registration.backends.default.DefaultBackend',
    #      'form_class': RegistrationFormUniqueEmail,
    #  }, name='registration_register'),

    (r'^accounts/', include('registration.urls')),

    url(r'^twitter/$',
        redirect_to,
        {'url': 'http://twitter.com/libercopy'},
        name='twitter'
       ),
    url(r'^facebook/$',
        redirect_to,
        {'url': 'https://www.facebook.com/pages/LiberCopy/182462775103017'},
        name='facebook'
       ),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^rosetta/', include('rosetta.urls')),
    )
