#pylint: disable-msg=R0201
from django.contrib import admin
from book import models as m

class LinkInline(admin.TabularInline):
    model = m.BookLink


class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug_name': ('name', )}
    inlines = [
        LinkInline,
    ]

admin.site.register(m.Book, BookAdmin)
admin.site.register(m.Category)
admin.site.register(m.ImageBook)
admin.site.register(m.BookLink)
admin.site.register(m.Author)
admin.site.register(m.BookLanguages)
