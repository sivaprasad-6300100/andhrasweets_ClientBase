from django.contrib import admin


# Register your models here.


from .models import Products
from .models import Banner
# from .models import Blog_Model



admin.site.register(Products)
admin.site.register(Banner)
# @admin.register(Blog_Model)
# class BlogAdmin(admin.ModelAdmin):
    # list_display = ('title', 'created_at', 'is_published')
    # prepopulated_fields = {'slug': ('title',)}

