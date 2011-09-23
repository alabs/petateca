# coding=utf-8
from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType


class StatItem(models.Model):
    type_of = models.ForeignKey('StatType')
    pub_date = models.DateTimeField(default=datetime.now) # on_save
    total = models.PositiveIntegerField()


class StatType(models.Model):
    ''' 
    Como el ContentType de un modelo dado puede repetirse 
    (por ejemplo para todos los links y todos los links activos)
    lo mejor es separarlo por el div que SI tiene que ser unico
    '''
    content_type = models.ForeignKey(ContentType)
    description = models.CharField(max_length=255)
    items = models.ForeignKey(StatItem, blank=True, null=True)
    #el ID del div que usamos para pintar el canvas
    chart_div = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.description

