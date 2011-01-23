# pylint: disable-msg=W0611,W0401
from django.conf.urls.defaults import *
from blog.models import Post

urlpatterns = patterns('blog.views',
    url(r'^$', 'index', name="blog-index"),
    url(r'^post/(?P<post_slug>[-\w]+)/$', 'get_post', name="get_post"),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', 'get_tag', name="get_tag"),
    (r'^comments/', include('django.contrib.comments.urls')),
)

blog_dict = {  
    'queryset': Post.objects.all(),
    'date_field': 'date',
}  

urlpatterns += patterns('django.views.generic.date_based',  
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[0-9A-Za-z-]+)/$', 'object_detail', dict(blog_dict, slug_field='slug')),  
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',  'archive_day', blog_dict),  
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',  'archive_month', blog_dict),  
    (r'^(?P<year>\d{4})/$',  'archive_year',  blog_dict),  
    (r'^/?$',  'archive_index', blog_dict), )

