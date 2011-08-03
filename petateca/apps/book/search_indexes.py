from haystack.indexes import SearchIndex, CharField
from haystack import site

from book.models import Book

class BookIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name')

site.register(Book, BookIndex)
