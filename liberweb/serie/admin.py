from django.contrib import admin
from .import models as m

class ImageInline(admin.TabularInline):
    model = m.ImageSerie

class SerieAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]

admin.site.register(m.Serie, SerieAdmin)
admin.site.register(m.Episode)
admin.site.register(m.Link)
admin.site.register(m.SubtitleLink)
admin.site.register(m.Languages)
admin.site.register(m.Network)
admin.site.register(m.Genre)
admin.site.register(m.Actor)
admin.site.register(m.ImageSerie)
admin.site.register(m.ImageActor)

