from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('blog.views',
    (r'^$', 'index'),
    url(r'^(?P<post_slug>[-\w]+)/$', 'get_post', name="get_post")
)

