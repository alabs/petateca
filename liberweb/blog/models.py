from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from datetime import datetime


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=64)
    date = models.DateTimeField(default=datetime.now)
    post = models.TextField()
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None):
        self.slug = slugify( self.title )
        super( Post, self ).save(force_insert, force_update, using)

class ImagePost(models.Model):
    title = models.CharField(max_length=100)
    src = models.ImageField(upload_to="img/blog")
    post = models.ForeignKey("Post", related_name="images")

    def __unicode__(self):
        return self.title
