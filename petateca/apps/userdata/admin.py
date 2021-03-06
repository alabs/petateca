from django.contrib import admin
from django.contrib.auth.models import User
#from django.contrib.auth.admin import UserAdmin

from .models import UserProfile, UserToInvite

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ("username", "email")
    list_display = ("username", "is_staff", "is_superuser", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
#    inlines = [UserProfileInline]

class UserToInviteAdmin(admin.ModelAdmin):
    search_fields = ('mail',)
    pass


admin.site.register(UserToInvite, UserToInviteAdmin)
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)

