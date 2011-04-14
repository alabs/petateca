# pylint: disable-msg=E1102
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=64)
    date = models.DateTimeField(default=datetime.now)
    post = models.TextField(help_text=_('Cuerpo del post'))
    slug = models.SlugField(unique=True)
    summary = models.TextField(
        max_length=200,
        help_text=_('Resumen del post que se ve en la principal')
    )
    tags = TaggableManager()

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None):
        self.slug = slugify(self.title)
        super(Post, self).save(force_insert, force_update, using)

    @models.permalink
    def get_absolute_url(self):
        return ('get_post', (),
                {'post_slug': self.slug, })


class ImagePost(models.Model):
    title = models.CharField(max_length=100)
    src = models.ImageField(upload_to="img/blog")
    post = models.ForeignKey("Post", related_name="images")

    def __unicode__(self):
        return self.title
