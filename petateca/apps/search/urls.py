from django.conf.urls.defaults import *

from haystack.views import SearchView, search_view_factory
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet


urlpatterns = patterns('search.views',
    (r'^$', search_view_factory(
        view_class=SearchView,
        searchqueryset=SearchQuerySet(),
        form_class=ModelSearchForm
    )),
    (r'^lookup/$', 'search_lookup'),
    (r'^opensearch/$', 'opensearch_lookup'),

)
