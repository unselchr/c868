from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models as models
from . import forms as forms

admin.site.register(models.Role)
admin.site.register(models.Part)

class CustomUserAdmin(UserAdmin):
    add_form = forms.CustomUserCreationForm
    form = forms.CustomUserChangeForm
    model = models.CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "role")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "role",
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(models.CustomUser, CustomUserAdmin)