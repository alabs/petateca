from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ("username", "email")
    list_display = ("username", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "is_active")
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)

