from django.contrib import admin
from .models import Order,OrderItem,Delivery

# Register your models here.

# admin order all details
class OrderItemInline(admin.TabularInline):
    model =OrderItem
    extra =0
    readonly_fields =('product','quantity','price')


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'get_user_phone',
        'address',
        'total_amount',
        'payment_method',
        'status',
        'created_at',
    )

    list_filter = ('payment_method', 'status')
    search_fields = ('user__username', 'address__full_name', 'address__phone_number')

    inlines = [OrderItemInline]

    def get_user_phone(self, obj):
        if obj.address:
            return obj.address.phone_number
        return "No Phone"
    get_user_phone.short_description = "Phone Number"


















@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')


# ========================delivery tracking admin========================

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'tracking_id', 'delivery_date', 'shipped_at', 'delivered_at')
    list_filter = ('delivery_date',)
