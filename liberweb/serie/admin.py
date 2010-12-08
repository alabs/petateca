from django.contrib import admin
from . import models as m

class ImageInline(admin.TabularInline):
    model = m.ImageSerie
    extra = 1
    list_display = ['my_image_thumb']


class EpisodeInline(admin.StackedInline):
    model = m.Episode

class SerieAdmin(admin.ModelAdmin):
    list_display = ['name', 'network', 'runtime',]
    list_filter = ('runtime', 'genres', 'network',)
    prepopulated_fields = {'slug_name': ('name', )}
    inlines = [
        #EpisodeInline,
        ImageInline,
    ]
    search_fields = ['name',]
    ordering       = ('name',)

admin.site.register(m.Serie, SerieAdmin)

class LinkInline(admin.TabularInline):
    model = m.Link

class EpisodeInline(admin.ModelAdmin):
    prepopulated_fields = {'slug_title': ('title', )}
    inlines = [
        LinkInline,
    ]

admin.site.register(m.Episode, EpisodeInline)

class SubtitleLinkInline(admin.TabularInline):
    model = m.SubtitleLink

class LinkAdmin(admin.ModelAdmin):
    inlines = [
        SubtitleLinkInline,
    ]

admin.site.register(m.Link, LinkAdmin)
admin.site.register(m.SubtitleLink)
admin.site.register(m.Languages)
admin.site.register(m.Network)

class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug_name': ('name', )}

admin.site.register(m.Genre, GenreAdmin)
admin.site.register(m.Actor)
admin.site.register(m.ImageSerie)
admin.site.register(m.ImageActor)

