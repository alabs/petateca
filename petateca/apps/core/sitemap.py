from django.contrib.sitemaps import Sitemap
from serie.models import Serie


class SerieSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Serie.objects.order_by("name_es")
