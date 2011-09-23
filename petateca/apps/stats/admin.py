from django.contrib import admin
from stats import models as m

class StatItemInline(admin.TabularInline):
    model = m.StatItem

class StatTypeAdmin(admin.ModelAdmin):
    list_display = ['description', 'content_type', 'chart_div']
    inlines = [ StatItemInline ]

admin.site.register(m.StatType, StatTypeAdmin)
