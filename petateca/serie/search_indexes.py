from haystack.indexes import SearchIndex, CharField
from haystack import site

from .models import Serie, Actor


class SerieIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name')
    name_es = CharField(model_attr='name_es')
    name_en = CharField(model_attr='name_en')
    description = CharField(model_attr='description', null=True)
    description_es = CharField(model_attr='description_es', null=True)
    description_en = CharField(model_attr='description_en', null=True)

site.register(Serie, SerieIndex)


class ActorIndex(SearchIndex):
    text = CharField(document=True, model_attr='name')
    name = CharField(model_attr='name')

site.register(Actor, ActorIndex)
