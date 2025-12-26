from django.contrib import admin
from .models import Blogs

@admin.register(Blogs)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
