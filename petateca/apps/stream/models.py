from django.db import models
#from django.contrib.contenttypes import generic
#from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType

from datetime import datetime


class StreamItem(models.Model):
    ''' Save content_type and total count of a given Model '''
    content_type = models.ForeignKey(ContentType)

    pub_date = models.DateTimeField(default=datetime.now) # on_save
    total = models.PositiveIntegerField()


def save_new(model):
    ''' Save content_type and total count of a given Model '''
    # Get the instance's content type
    ctype = ContentType.objects.get_for_model(model)
    count = model.objects.count()
    StreamItem.objects.get_or_create(content_type=ctype, total=count)


# COMO FUNCIONA
#
#from django.contrib.auth.models import User
#from apps.serie.models import Serie, Link, LinkSeason
#from apps.book.models import Book, BookLink
#
#item_list = [ User, Serie, Link, LinkSeason, Book, BookLink ]
#
#for item in item_list:
#    save_new(item)
