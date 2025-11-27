from django.contrib import admin

# Register your models here.


from .models import Products
from .models import Banner



admin.site.register(Products)
admin.site.register(Banner)

