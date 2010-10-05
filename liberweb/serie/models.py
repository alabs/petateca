from django.db import models

class Serie(models.Model):
    name = models.CharField(max_length=255)
    slug_name = models.SlugField()
    network = models.ForeignKey("Network", related_name="series")
    genre = models.ForeignKey("Genre")
    runtime = models.IntegerField()
    actors = models.ManyToManyField("Actor")
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Episode(models.Model):
    air_date = models.DateField()
    title = models.CharField(max_length=255)
    slug_title = models.SlugField()
    season = models.IntegerField()
    episode = models.IntegerField()
    description = models.TextField()

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
    link = models.ForeignKey("Link")

    def __unicode__(self):
        return self.url

class Languages(models.Model):
    iso_code = models.CharField(max_length=2)

    def __unicode__(self):
        return self.iso_code

class Network(models.Model):
    name = models.CharField(max_length=25)
    url = models.URLField(null=True)

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
    creator = models.CharField(max_length=100)
    is_poster = models.BooleanField()
    serie = models.ForeignKey("Serie")

    def __unicode__(self):
        return self.title

class ImageActor(models.Model):
    title = models.CharField(max_length=100)
    src = models.ImageField(upload_to="/img/actor")
    creator = models.CharField(max_length=100)
    is_poster = models.BooleanField()
    actor = models.ForeignKey("Actor")

    def __unicode__(self):
        return self.title

