from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from djangoratings.fields import RatingField
from datetime import datetime


class Serie(models.Model):
    name = models.CharField(max_length=255)
    slug_name = models.SlugField(unique=True, help_text=_('name in URL'))
    network = models.ForeignKey("Network", related_name="series")
    genres = models.ManyToManyField("Genre", related_name="series")
    runtime = models.IntegerField(
        name=_('runtime duration'),
        blank=True,
        null=True,
        help_text=_('duration of episodes in minutes')
    )
    actors = models.ManyToManyField("Actor", through='Role')
    description = models.TextField()
    rating = models.FloatField(
        blank=True,
        null=True,
        help_text=('rating from eztv')
    )
    rating_count = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    rating_user = RatingField(range=5, can_change_vote=True)

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None):
        self.slug_name = slugify(self.name)
        super(Serie, self).save(force_insert, force_update, using)

    @models.permalink
    def get_absolute_url(self):
        return ('liberweb.serie.views.get_serie', (),
                {'serie_slug': self.slug_name, })


class Role(models.Model):
    serie = models.ForeignKey("Serie")
    actor = models.ForeignKey("Actor")
    sortorder = models.IntegerField(blank=True, null=True)
    role = models.CharField(max_length=255)

    class Meta:
        unique_together = ("serie", "actor", "role")


class SerieAlias(models.Model):
    name = models.CharField(max_length=255, unique=True)
    serie = models.ForeignKey("Serie", related_name="aliases")


class Episode(models.Model):
    serie = models.ForeignKey('Serie', related_name="episodes")
    air_date = models.DateField(
        _('air date'),
        blank=True,
        null=True,
        help_text=_('first broadcast date')
    )
    title = models.CharField(max_length=255)
    slug_title = models.SlugField(unique=False)
    season = models.IntegerField()
    episode = models.IntegerField()
    description = models.TextField()
    created_time = models.DateField(auto_now_add=True)
    modified_time = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.slug_title:
            self.slug_title = slugify(self.title)
        super(Episode, self).save(force_insert, force_update, using)

    @models.permalink
    def get_absolute_url(self):
        return ('liberweb.serie.views.get_episode', (), {
                'serie_slug': self.serie.slug_name,
                'season': self.season,
                'episode': self.episode,
        })


class Link(models.Model):
    episode = models.ForeignKey("Episode", related_name="links")
    url = models.CharField(max_length=255, unique=True, db_index=True)
    audio_lang = models.ForeignKey("Languages", related_name="audio_langs")
    subtitle = models.ForeignKey(
       "Languages",
       related_name="sub_langs",
       null=True,
       blank=True,
       help_text=_("integrated subtitles")
    )
    bot = models.CharField(max_length=255, null=True, blank=True)
    pub_date = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.url


class SubtitleLink(models.Model):
    url = models.CharField(max_length=255)
    lang = models.ForeignKey("Languages")
    link = models.ForeignKey("Link", related_name="subtitles")

    def __unicode__(self):
        return self.url


class Languages(models.Model):
    iso_code = models.CharField(max_length=2)
    country = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        unique_together = ("iso_code", "country")

    def __unicode__(self):
        if self.country:
            return "%s-%s" % (self.iso_code, self.country)
        return self.iso_code


class Network(models.Model):
    name = models.CharField(max_length=25)
    url = models.URLField(null=True, blank=True)
    slug_name = models.SlugField(unique=True)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super(Network, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('liberweb.serie.views.get_network', [str(self.slug_name)])


class Genre(models.Model):
    name = models.CharField(max_length=25)
    slug_name = models.SlugField(unique=True)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super(Genre, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('liberweb.serie.views.get_genre', [str(self.slug_name)])


class Actor(models.Model):
    name = models.CharField(max_length=100)
    slug_name = models.SlugField(unique=True)

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super(Actor, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('liberweb.serie.views.get_actor', [str(self.slug_name)])


class IsPosterManager(models.Manager):
    def get_is_poster(self):
        return self.filter(is_poster=True)


class ImageSerie(models.Model):
    title = models.CharField(max_length=100)
    src = models.ImageField(upload_to="img/serie")
    creator = models.CharField(max_length=100, null=True, blank=True)
    is_poster = models.BooleanField()
    serie = models.ForeignKey("Serie", related_name="images")
    get_is_poster = IsPosterManager()

    def __unicode__(self):
        return self.title


class ImageActor(models.Model):
    title = models.CharField(max_length=100)
    src = models.ImageField(upload_to="img/actor")
    creator = models.CharField(max_length=100, null=True, blank=True)
    is_poster = models.BooleanField()
    actor = models.ForeignKey("Actor", related_name="images")

    def __unicode__(self):
        return self.title


class ImageEpisode(models.Model):
    title = models.CharField(max_length=100)
    src = models.ImageField(upload_to="img/episodes")
    creator = models.CharField(max_length=100, null=True, blank=True)
    is_poster = models.BooleanField()
    episode = models.ForeignKey("Episode", related_name="images")
    get_is_poster = IsPosterManager()

    def __unicode__(self):
        return self.title
