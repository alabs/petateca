from django.contrib import admin
from liberweb.blog.models import Post, ImagePost
from .import models as m


class ImageInline(admin.TabularInline):
    model = ImagePost
    extra = 1

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    inlines = [
        #EpisodeInline,
        ImageInline,
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(ImagePost)

