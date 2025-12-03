from django.contrib import admin
from .models import UserProfile,Cart

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'is_verified', 'created_at')
    search_fields = ('name', 'phone')
    readonly_fields = ('created_at',)


admin.site.register(Cart)
