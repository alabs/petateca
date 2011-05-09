from haystack.indexes import SearchIndex, CharField
from haystack import site

from serie.models import Serie

class SerieIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name', boost=1.125)
    name_es = CharField(model_attr='name_es')
    name_en = CharField(model_attr='name_en')

site.register(Serie, SerieIndex)
