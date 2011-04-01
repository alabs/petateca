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


class SeasonInline(admin.TabularInline):
    model = m.Season


class SerieAdmin(admin.ModelAdmin):
    list_display = ['name', 'network', 'runtime', 'image_serie_serie', ]
    list_filter = ('runtime', 'genres', 'network', )
    prepopulated_fields = {'slug_name': ('name', )}
    inlines = [
        SeasonInline,
    ]
    search_fields = ['name', ]
    ordering = ('name', )
    def image_serie_serie(self, obj):
        try:
            img = obj.images.all()[0]
            file_img = img.src.file
            thumb = default.backend.get_thumbnail(file_img, ADMIN_THUMBS_SIZE)
            return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
        except:
            return "No Image"
    image_serie_serie.short_description = 'Thumbnail'  #pylint: disable-msg=W0612
    image_serie_serie.allow_tags = True  #pylint: disable-msg=W0612



class LinkInline(admin.TabularInline):
    model = m.Link


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['title', 'season', 'episode', ]


class SubtitleLinkInline(admin.TabularInline):
    model = m.SubtitleLink


class LinkAdmin(admin.ModelAdmin):
    list_display = [
        'url',
        'episode',
        'get_epi_season',
        'get_epi_number',
        'get_serie',
        'user',
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

    get_serie.short_description = 'Serie'  #pylint: disable-msg=W0612
    get_epi_season.short_description = 'Season'  #pylint: disable-msg=W0612
    get_epi_number.short_description = 'Episode'  #pylint: disable-msg=W0612



class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug_name': ('name', )}


class ImageSerieAdmin(admin.ModelAdmin):
    model = m.ImageSerie
    list_display = ['title', 'serie', 'image_serie', ]

    def image_serie(self, obj):
        try:
            img = obj.src.file
            thumb = default.backend.get_thumbnail(img, ADMIN_THUMBS_SIZE)
            return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
        except:
            return "No Image"
    
    image_serie.short_description = 'Thumbnail'  #pylint: disable-msg=W0612
    image_serie.allow_tags = True  #pylint: disable-msg=W0612


class SeasonImageInline(admin.TabularInline):
    model = m.ImageSeason
    extra = 1


class SeasonAdmin(admin.ModelAdmin):
    model = m.Season
    inlines = [
        SeasonImageInline,
        EpisodeInline,
    ]



admin.site.register(m.Actor)
admin.site.register(m.Role)
admin.site.register(m.Episode, EpisodeAdmin)
admin.site.register(m.Genre, GenreAdmin)
admin.site.register(m.ImageActor)
admin.site.register(m.ImageEpisode)
admin.site.register(m.ImageSerie, ImageSerieAdmin)
admin.site.register(m.Languages)
admin.site.register(m.Link, LinkAdmin)
admin.site.register(m.Network)
admin.site.register(m.Serie, SerieAdmin)
admin.site.register(m.Season, SeasonAdmin)
admin.site.register(m.SubtitleLink)
admin.site.register(m.ImageSeason)
