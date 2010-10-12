from django.db import models
from django.utils.translation import ugettext_lazy as _

class Serie(models.Model):
    name = models.CharField(max_length=255)
    slug_name = models.SlugField()
    network = models.ForeignKey("Network", related_name="series")
    genres = models.ManyToManyField("Genre", related_name="series")
    runtime = models.IntegerField(_('Runtime duration'), blank=True, null=True, help_text=_('duration of episodes in minutes'))
    actors = models.ManyToManyField("Actor")
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Episode(models.Model):
    serie = models.ForeignKey('Serie', related_name="episodes")
    air_date = models.DateField(_('Air date'), blank=True, null=True, help_text=_('first broadcast date'))
    title = models.CharField(max_length=255)
    slug_title = models.SlugField()
    season = models.IntegerField()
    episode = models.IntegerField()
    description = models.TextField()
    created_time = models.DateField(auto_now_add=True)
    modified_time = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.title

class Link(models.Model):
    episode = models.ForeignKey("Episode", related_name="links")
    url = models.CharField(max_length=255)
    audio_lang = models.ForeignKey("Languages", related_name="audio_langs")
    subtitle = models.ForeignKey("Languages", related_name="sub_langs", null=True) #Integrated subtitles

    def __unicode__(self):
        return self.url

class SubtitleLink(models.Model):
    url = models.CharField(max_length=255)
    lang = models.ForeignKey("Languages")
    link = models.ForeignKey("Link", related_name="subtitles")

    def __unicode__(self):
        return self.url

class Languages(models.Model):
    iso_code = models.CharField(max_length=2, unique=True)

    def __unicode__(self):
        return self.iso_code

class Network(models.Model):
    name = models.CharField(max_length=25)
    url = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=25)
    slug_name = models.SlugField()

    def __unicode__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class ImageSerie(models.Model):
    title = models.CharField(max_length=100)
    src = models.ImageField(upload_to="/img/serie")
    creator = models.CharField(max_length=100, null=True, blank=True)
    is_poster = models.BooleanField()
    serie = models.ForeignKey("Serie", related_name="images")

    def __unicode__(self):
        return self.title

class ImageActor(models.Model):
    title = models.CharField(max_length=100)
    src = models.ImageField(upload_to="/img/actor")
    creator = models.CharField(max_length=100, null=True, blank=True)
    is_poster = models.BooleanField()
    actor = models.ForeignKey("Actor", related_name="images")

    def __unicode__(self):
        return self.title

