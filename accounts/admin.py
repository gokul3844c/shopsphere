from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "get_phone")

    def get_phone(self, instance):
        if hasattr(instance, "profile"):
            return instance.profile.phone
        return ""
    get_phone.short_description = "Phone"

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
