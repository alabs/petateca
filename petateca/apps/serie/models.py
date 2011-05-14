# -*- coding: utf-8 -*-
# pylint: disable-msg=E1102
from datetime import datetime

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User

from djangoratings.fields import RatingField
from voting.models import Vote 
#XXX: poster deberia ser on_delete null en vez de cascade


class Serie(models.Model):
    name = models.CharField(max_length=255)
    slug_name = models.SlugField(unique=True, help_text=_('nombre en la URL'))
    network = models.ForeignKey("Network", related_name="series")
    genres = models.ManyToManyField("Genre", related_name="series")
    runtime = models.IntegerField(
        name=_('duracion de los episodios'),
        blank=True,
        null=True,
        help_text=_( 'duracion del episodio en minutos' )
    )
    actors = models.ManyToManyField(
        "Actor", 
        through='Role',
        help_text=_('actores que trabajaron en la serie'))
    description = models.TextField()
    finished = models.BooleanField(
        default=False,
        help_text=_('la serie ha finalizado?')
    )
    rating = RatingField(
        range=5,
        can_change_vote=True,
        help_text=_('puntuacion de estrellas')
    )
    poster = models.OneToOneField(
        'ImageSerie',
        related_name='poster_of',
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None):
        ''' When is saved, the title is converted to slug - aka URL'''
        self.slug_name = slugify(self.name)
        super(Serie, self).save(force_insert, force_update, using)

    @models.permalink
    def get_absolute_url(self):
        return ('serie.views.get_serie', (),
                {'serie_slug': self.slug_name, })


class Role(models.Model):
    serie = models.ForeignKey("Serie")
    actor = models.ForeignKey("Actor")
    sortorder = models.IntegerField(blank=True, null=True)
    role = models.CharField(
        max_length=255,
        help_text=_('personaje que el actor ha hecho en la serie')
    )

    class Meta:
        unique_together = ("serie", "actor", "role")

    def __unicode__(self):
        return self.role


class SerieAlias(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('otros nombres para la misma serie')
    )
    serie = models.ForeignKey("Serie", related_name="aliases")


class Season(models.Model):
    serie = models.ForeignKey('Serie', related_name="season")
    season = models.IntegerField(
        help_text=_('numero de temporada para la serie')
    )
    poster = models.OneToOneField(
        'ImageSeason',
        related_name='poster_of',
        null=True,
        blank=True
    )

    def get_next_season(self):
        next_season = self.season + 1
        try:
            return Season.objects.get(season=next_season, serie=self.serie)
        except:
            return None

    def get_previous_season(self):
        prev_season = self.season - 1
        try:
            return Season.objects.get(season=prev_season, serie=self.serie)
        except:
            return None

    def __unicode__(self):
        ''' Serie Name - Season '''
        return self.serie.name + ' - ' + str(self.season)

    @models.permalink
    def get_absolute_url(self):
        return ('serie.ajax.season_lookup', (), {
                'serie_id': self.serie.id,
                'season': self.season,
        })

    @models.permalink
    def get_season(self):
        return ('serie.ajax.season_full_links_lookup', (), {
                'serie_slug': self.serie.slug_name,
                'season': self.season,
        })


class ImageSeason(models.Model):
    title = models.CharField(max_length=100)
    src = models.ImageField(upload_to="img/season")
    creator = models.CharField(max_length=100, null=True, blank=True)
    is_poster = models.BooleanField(
        help_text=_('entre varias imagenes, cual es el poster?')
    )
    season = models.ForeignKey("Season", related_name="images")
    objects = models.Manager()

    def __unicode__(self):
        return self.title


def get_default_user_for_links():
    default_user = settings.DEFAULT_USER_FOR_LINKS
    try:
        user = User.objects.get(username=default_user)
        return user
    except User.DoesNotExist:
        raise NameError(
            "Debes crear un usuario valido para DEFAULT_USER_FOR_LINKS llamado %s" % (default_user)
        )


class LinkSeason(models.Model):
    season = models.ForeignKey("Season", related_name="links", editable=False)
    url = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="URL"
    )
    audio_lang = models.ForeignKey("Languages", related_name="audio_langs_season", verbose_name="Idioma")
    subtitle = models.ForeignKey(
       "Languages",
       related_name="sub_langs_season",
       null=True,
       blank=True,
       verbose_name="Subtitulos",
    )
    user = models.ForeignKey(
        User,
        related_name="user",
        editable=False,
        default=get_default_user_for_links
    )
    pub_date = models.DateTimeField(default=datetime.now, editable=False)

    def __unicode__(self):
        return self.url


class Episode(models.Model):
    season = models.ForeignKey(
        'Season',
        related_name="episodes",
        editable=False
    )
    air_date = models.DateField(
        _('Fecha de emision'),
        blank=True,
        null=True,
    )
    title = models.CharField(
        _('Titulo'),
        max_length=255
    )
    episode = models.IntegerField(
        _('Episodio'),
        help_text=_( 'Numero de episodio en temporada' ) 
    )
    description = models.TextField()
    created_time = models.DateField(auto_now_add=True)
    modified_time = models.DateField(auto_now=True)
    poster = models.OneToOneField(
        'ImageEpisode',
        related_name='poster_of',
        null=True,
        blank=True,
        editable=False
    )

    def get_next_episode(self):
        next_epi = self.episode + 1
        try:
            return Episode.objects.get(episode=next_epi, season=self.season)
        except:
            return None

    def get_previous_episode(self):
        prev_epi = self.episode - 1
        try:
            return Episode.objects.get(episode=prev_epi, season=self.season)
        except:
            return None

    def season_episode(self):
        return "S%02dE%02d" % (self.season.season, self.episode)
            
    def get_absolute_url(self):
        return '/serie/%s/episode/S%02dE%02d/' % (
            self.season.serie.slug_name, 
            self.season.season,
            self.episode
        )

    def get_add_link_url(self):
        return '/serie/%s/episode/S%02dE%02d/add/' % (
            self.season.serie.slug_name, 
            self.season.season,
            self.episode
        )

    def from_future(self):
        now = datetime.now().date()
        air_date = self.air_date
        if now < air_date:
            return 'future'
        else:
            return ''

    def __unicode__(self):
        return self.title


class Link(models.Model):
    episode = models.ForeignKey(
        "Episode",
        related_name="links",
        editable=False
    )
    url = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="URL"
    )
    audio_lang = models.ForeignKey(
        "Languages",
        related_name="audio_langs",
        verbose_name="Idioma"
    )
    subtitle = models.ForeignKey(
       "Languages",
       related_name="sub_langs",
       null=True,
       blank=True,
       verbose_name="Subtitulos",
    )
    user = models.ForeignKey(
        User,
        related_name="link_user",
        editable=False,
        default=get_default_user_for_links
    )
    pub_date = models.DateTimeField(
        default=datetime.now,
        help_text=_('cuando se ha subido el link? por defecto cuando se guarda'),
        editable=False
    )

    def __unicode__(self):
        return self.url

    def get_score(self):
        return Vote.objects.get_score(self)['score']


class SubtitleLink(models.Model):
    ''' For external subtitles '''
    url = models.CharField(max_length=255)
    lang = models.ForeignKey("Languages")
    link = models.ForeignKey("Link", related_name="subtitles")

    def __unicode__(self):
        return self.url


class Languages(models.Model):
    ''' Languages for links '''
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
    slug_name = models.SlugField(unique=True, help_text=_('nombre en URL'))

    def save(self, force_insert=False, force_update=False, using=None):
        ''' When is saved, the name is converted to slug - aka URL'''
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super(Network, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=25)
    slug_name = models.SlugField(unique=True, help_text=_('nombre en URL'))

    def save(self, force_insert=False, force_update=False, using=None):
        ''' When is saved, the name is converted to slug - aka URL'''
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super(Genre, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100)
    slug_name = models.SlugField(unique=True, help_text=_('nombre en URL'))
    poster = models.OneToOneField(
        'ImageActor',
        related_name='poster_of',
        null=True,
        blank=True
    )

    def save(self, force_insert=False, force_update=False, using=None):
        ''' When is saved, the name is converted to slug - aka URL'''
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super(Actor, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('get_actor', [str(self.slug_name)])


class ImageSerie(models.Model):
    title = models.CharField(max_length=100)
    src = models.ImageField(upload_to="img/serie")
    creator = models.CharField(max_length=100, null=True, blank=True)
    is_poster = models.BooleanField(
        help_text=_('entre varias imagenes, cual es el poster?')
    )
    serie = models.ForeignKey("Serie", related_name="images")
    objects = models.Manager()

    def __unicode__(self):
        return self.title


class ImageActor(models.Model):
    title = models.CharField(max_length=100)
    src = models.ImageField(upload_to="img/actor")
    creator = models.CharField(max_length=100, null=True, blank=True)
    is_poster = models.BooleanField(
        help_text=_('entre varias imagenes, cual es el poster?')
    )
    actor = models.ForeignKey("Actor", related_name="images")
    objects = models.Manager()

    def __unicode__(self):
        return self.title


class ImageEpisode(models.Model):
    title = models.CharField(max_length=100)
    src = models.ImageField(upload_to="img/episodes")
    creator = models.CharField(max_length=100, null=True, blank=True)
    is_poster = models.BooleanField(
        help_text=_('entre varias imagenes, cual es el poster?')
    )
    episode = models.ForeignKey("Episode", related_name="images")
    objects = models.Manager()

    def __unicode__(self):
        return self.title


poster_dispatch = {
    ImageSerie: "serie",
    ImageSeason: "season",
    ImageEpisode: "episode",
    ImageActor: "actor",
}


def update_poster(sender, instance, **kwargs):
    obj = getattr(instance, poster_dispatch[sender])
    if instance.is_poster:
        obj.poster = instance
    else:
        other_poster = sender.objects.filter(**{poster_dispatch[sender]:obj, "is_poster":True}).all()
        if other_poster:
            obj.poster = other_poster[0]
        else:
            obj.poster = None
    obj.save()

def delete_poster(sender, instance, **kwargs):
    obj = getattr(instance, poster_dispatch[sender])
    other_poster = sender.objects.filter(**{poster_dispatch[sender]:obj, "is_poster":True}).all()
    if other_poster:
        obj.poster = other_poster[0]
    else:
        obj.poster = None
    obj.save()


for sender in poster_dispatch.keys():
    post_save.connect(update_poster, sender=sender)
    post_delete.connect(update_poster, sender=sender)

