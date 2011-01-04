from django.contrib.syndication.views import Feed
from liberweb.serie.models import Link
from liberweb.blog.models import Post
from django.utils.feedgenerator import Atom1Feed


class RSSLatestLinksFeed(Feed):
    # pylint: disable-msg=R0201
    title = "LiberCopy lastest serie links"
    link = "/series/"
    description = "Lastest added links to LC"

    def items(self):
        return Link.objects.order_by('-pub_date')[:10]

    def item_title(self, item):
        return item.episode

    def item_description(self, item):
        return item.url

    def item_link(self, item):
        return item.episode.get_absolute_url()

   # episode = models.ForeignKey("Episode", related_name="links")
   # url = models.CharField(max_length=255, unique=True, db_index=True)
   # audio_lang = models.ForeignKey("Languages", related_name="audio_langs")
   # subtitle


class AtomLatestLinksFeed(RSSLatestLinksFeed):
    feed_type = Atom1Feed
    subtitle = RSSLatestLinksFeed.description


class RSSBlogFeed(Feed):
    # pylint: disable-msg=R0201
    title = "LiberCopy lastest blog post"
    link = "/blog/"
    description = "Lastest blog post on LC"

    def items(self):
        return Post.objects.order_by('date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.post

    def item_link(self, item):
        return '/'


class AtomBlogFeed(RSSBlogFeed):
    feed_type = Atom1Feed
    subtitle = RSSBlogFeed.description
