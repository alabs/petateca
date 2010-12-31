from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('blog.views',
    url(r'^$', 'index', name="blog-index"),
    url(r'^(?P<post_slug>[-\w]+)/$', 'get_post', name="get_post"),
    (r'^comments/', include('django.contrib.comments.urls')),
)
