#pylint: disable-msg=R0201
from django.contrib import admin
from . import models as m

from sorl.thumbnail import default
ADMIN_THUMBS_SIZE = '60x60'


class ImageInline(admin.TabularInline):
    model = m.ImageSerie
    extra = 1


class EpisodeInline(admin.TabularInline):
    model = m.Episode

#class EpisodeInline(admin.ModelAdmin):
#    prepopulated_fields = {'slug_title': ('title', )}
#    inlines = [
#        LinkInline,
#    ]


class SerieAdmin(admin.ModelAdmin):
    list_display = ['name', 'network', 'runtime', 'image_serie_serie', ]
    list_filter = ('runtime', 'genres', 'network', )
    prepopulated_fields = {'slug_name': ('name', )}
    inlines = [
        ImageInline,
        EpisodeInline,
    ]

    def image_serie_serie(self, obj):
        img = obj.images.get_is_poster()[0]
        file = img.src.file
        if file:
            thumb = default.backend.get_thumbnail(file, ADMIN_THUMBS_SIZE)
            return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
        else:
            return "No Image"
    image_serie_serie.short_description = 'Thumbnail'
    image_serie_serie.allow_tags = True
    search_fields = ['name', ]
    ordering = ('name', )


class LinkInline(admin.TabularInline):
    model = m.Link


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['title', 'serie', 'season', 'episode', ]


class SubtitleLinkInline(admin.TabularInline):
    model = m.SubtitleLink


class LinkAdmin(admin.ModelAdmin):
    list_display = [
        'url',
        'episode',
        'get_epi_season',
        'get_epi_number',
        'get_serie',
        'bot',
    ]
    inlines = [
        SubtitleLinkInline,
    ]

    def get_serie(self, obj):
        return '%s' % (obj.episode.serie)

    def get_epi_season(self, obj):
        return '%s' % (obj.episode.season)

    def get_epi_number(self, obj):
        return '%s' % (obj.episode.episode)

    get_serie.short_description = 'Serie'
    get_epi_season.short_description = 'Season'
    get_epi_number.short_description = 'Episode'


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug_name': ('name', )}


class ImageSerieAdmin(admin.ModelAdmin):
    model = m.ImageSerie
    list_display = ['title', 'serie', 'image_serie', ]

    def image_serie(self, obj):
        img = obj.src.file
        if img:
            thumb = default.backend.get_thumbnail(img, ADMIN_THUMBS_SIZE)
            return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
        else:
            return "No Image"

    image_serie.short_description = 'Thumbnail'
    image_serie.allow_tags = True

admin.site.register(m.Actor)
admin.site.register(m.Episode, EpisodeAdmin)
admin.site.register(m.Genre, GenreAdmin)
admin.site.register(m.ImageActor)
admin.site.register(m.ImageEpisode)
admin.site.register(m.ImageSerie, ImageSerieAdmin)
admin.site.register(m.Languages)
admin.site.register(m.Link, LinkAdmin)
admin.site.register(m.Network)
admin.site.register(m.Serie, SerieAdmin)
admin.site.register(m.SubtitleLink)
