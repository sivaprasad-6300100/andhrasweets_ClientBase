from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile,UserAddress

class UserProfileAdmin(UserAdmin):
    model = UserProfile

    # Fields shown in admin list page
    list_display = ('phone', 'name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    # Fields in the admin user edit page
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Personal Info", {"fields": ("name", "otp")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    # Fields to show while creating a new user in admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "name", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("phone", "name")
    ordering = ("phone",)


admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(Address)
admin.site.register(UserAddress)# Register the new model

