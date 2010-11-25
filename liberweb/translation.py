from modeltranslation.translator import translator, TranslationOptions
from liberweb.serie.models import Serie, Episode, Genre
from liberweb.blog.models import Post

class SerieTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

translator.register(Serie, SerieTranslationOptions)

class EpisodeTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

translator.register(Episode, EpisodeTranslationOptions)

class GenreTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Genre, GenreTranslationOptions)

class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'post',)

translator.register(Post, PostTranslationOptions)
