from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangoratings.fields import RatingField
from django.template.defaultfilters import slugify
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from voting.models import Vote 
from django.db.models import Sum
from generic_aggregation import generic_annotate

from core.lib.strip_accents import strip_accents

class SorterManager(models.Manager):
    def sorted_by_votes(self):
        return generic_annotate(self, Vote.object, Sum('vote')) 

def get_default_user_for_links():
    default_user = settings.DEFAULT_USER_FOR_LINKS
    try:
        user = User.objects.get(username=default_user)
        return user
    except User.DoesNotExist:
        raise NameError(
            "Debes crear un usuario valido para DEFAULT_USER_FOR_LINKS llamado %s" % (default_user)
        )


class Book(models.Model):
    name = models.CharField(max_length=255)
    slug_name = models.SlugField(unique=True, help_text=_('nombre en la URL'))
    category = models.ManyToManyField("Category", related_name="books")
    author = models.ManyToManyField(
        "Author", 
        related_name="books",
        null=True,
        blank=True,
        help_text=_('autores que escribieron el libro')
    )
    description = models.TextField()
    pub_date = models.DateTimeField(default=datetime.now, editable=False)
    isbn = models.CharField(null=True, blank=True, max_length=20)
    rating = RatingField(
        range=5,
        can_change_vote=True,
        allow_delete=True,
        help_text=_('puntuacion de estrellas')
    )
    poster = models.OneToOneField(
        'ImageBook',
        related_name='poster_of',
        null=True,
        blank=True
    )

#    def url(self):
#        ''' Devuelve la URL para la API (version 2) '''
#        return get_urlprefix() + reverse('API_v2_serie_detail', 
#            kwargs={'serie_id': self.pk})

    def ascii_name(self):
        return strip_accents(self.name)

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None):
        ''' When is saved, the title is converted to slug - aka URL'''
        self.slug_name = slugify(self.name)
        super(Book, self).save(force_insert, force_update, using)

    @models.permalink
    def get_absolute_url(self):
        return ('book.views.get_book', (),
                {'book_slug': self.slug_name, })


class Category(models.Model):
    name = models.CharField(max_length=25)
    slug_name = models.SlugField(unique=True, help_text=_('nombre en URL'))

    def save(self, force_insert=False, force_update=False, using=None):
        ''' When is saved, the name is converted to slug - aka URL'''
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super(Category, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return self.name


class ImageBook(models.Model):
    title = models.CharField(max_length=100)
    src = models.ImageField(upload_to="img/book")
    creator = models.CharField(max_length=100, null=True, blank=True)
    is_poster = models.BooleanField(
        help_text=_('entre varias imagenes, cual es el poster?')
    )
    book = models.ForeignKey("Book", related_name="images")
    objects = models.Manager()

#    def thumbnail(self):
#        ''' Para la API, conseguir thumbnail '''
#        urlprefix = get_urlprefix()
#        return urlprefix + get_thumbnail(self.src, '400x300').url

    def __unicode__(self):
        return self.title


class BookLink(models.Model):
    book = models.ForeignKey(
        "Book",
        related_name="links",
        editable=False
    )
    url = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="URL"
    )
    lang = models.ForeignKey(
        "BookLanguages",
        related_name="langs",
        verbose_name="Idioma"
    )
    # FIXME: :(
#    user = models.ForeignKey(
#        User,
#        related_name="booklink_user",
#        editable=False,
#        default=get_default_user_for_links
#    )
# TODO: formatos
    pub_date = models.DateTimeField(
        default=datetime.now,
        help_text=_('cuando se ha subido el link? por defecto cuando se guarda'),
        editable=False
    )
    # For link checker, so it can deactivate and/or change the check_date
    is_active = models.BooleanField(default=True, editable=False)
    check_date = models.DateTimeField(null=True, blank=True, editable=False)
    objects = SorterManager()

    def __unicode__(self):
        return self.url

    def get_score(self):
        return Vote.objects.get_score(self)['score']


class Author(models.Model):
    name = models.CharField(max_length=100)
    slug_name = models.SlugField(unique=True, help_text=_('nombre en URL'))
#    book = models.ForeignKey("Book", related_name="books")

    def save(self, force_insert=False, force_update=False, using=None):
        ''' When is saved, the name is converted to slug - aka URL'''
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super(Author, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return self.name

#    @models.permalink
#    def get_absolute_url(self):
#        return ('get_actor', [str(self.slug_name)])


class BookLanguages(models.Model):
    ''' Languages for links '''
    iso_code = models.CharField(max_length=2)
    country = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        unique_together = ("iso_code", "country")

    def __unicode__(self):
        if self.country:
            return "%s-%s" % (self.iso_code, self.country)
        return self.iso_code
