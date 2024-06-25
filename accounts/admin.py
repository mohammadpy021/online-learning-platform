from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Concat
from django.contrib import admin
from .models import User

# @admin.register(Profile)
# class CustomProfile(admin.ModelAdmin):
#     list_display = ("first_name",)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "full_name", "is_verified", "is_staff", "is_superuser",)
    def full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "courses",
                    "groups",
                    "user_permissions",
                    
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
            (
                None,
                {
                    "classes": ("wide",),
                    "fields": ("email", "password1", "password2"),
                },
            ),
        )




