from django.contrib import admin

# Register your models here.

from .models import Review_Model

from django.contrib import admin
from .models import Review_Model

@admin.register(Review_Model)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__phone', 'name', 'comment')

    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('product', 'user', 'name', 'rating', 'comment')
        }),
        ('Date Info', {
            'fields': ('created_at',),
        }),
    )
