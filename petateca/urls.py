from django.conf.urls.defaults import *
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

from django.conf import settings
from registration.forms import RegistrationFormTermsOfService
from invitation.views import register 
from django.contrib.auth import views as auth_views

from serie.sitemap import SerieSitemap

sitemaps = {
    'serie': SerieSitemap
}


urlpatterns = patterns('',
    (r'^$', 'views.index'),

    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),

    (r'^sentry/', include('sentry.urls')),

    (r'^serie/', include('serie.urls.obj')),
    (r'^series/', include('serie.urls.entity')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^blog/', include('blog.urls')),

    (r'^search/lookup/$', 'search.views.search_lookup'),

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

    (r'^accounts/', include('invitation.urls')),
    (r'^accounts/profile/$', 'userdata.views.view_profile'),
    # invitation
    url(r'^accounts/register/$',
        register,
        {
            'form_class': RegistrationFormTermsOfService,
            'backend': 'invitation.backends.InvitationBackend',
        },
        name='registration_register'),
    url(r'^accounts/signin/$',
        auth_views.login,
        {'template_name': 'registration/signin.html'},
        name='auth_login'),
    (r'^accounts/', include('registration.urls')),
    url(r'^user/(?P<user_name>[-\w]+)$', 'userdata.views.get_user_public_profile', name='get_user_public_profile'),
    (r'^avatar/', include('avatar.urls')),

    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^rosetta/', include('rosetta.urls')),
    )
