from django.contrib import admin
from liberweb.blog.models import Post, ImagePost

class ImageInline(admin.TabularInline):
    model = ImagePost
    extra = 1

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    inlines = [
        #EpisodeInline,
        ImageInline,
    ]
    list_display = ['title', 'slug', 'summary',]

    class Media:
        js = ('js/tiny_mce/tiny_mce.js',
              'js/tiny_mce/textareas.js',)

admin.site.register(Post, PostAdmin)
admin.site.register(ImagePost)

