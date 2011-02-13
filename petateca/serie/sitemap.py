from django.contrib.sitemaps import Sitemap
from serie.models import Serie
import datetime


class SerieSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Serie.objects.all()
