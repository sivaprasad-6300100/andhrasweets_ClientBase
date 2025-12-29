from django.db import models
from django.conf import settings   # <-- IMPORTANT
from products.models import Products
from users.models import UserAddress


class Order(models.Model):

    PAYMENT_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('ONLINE','ONLINE'),
        ('PHONEPE', 'PhonePe'),
        ('GPAY', 'Google Pay'),
        ('UPI', 'UPI'),
        ('PAYTM', 'Paytm'),
    )
    payment_status = models.CharField(
    max_length=20,
    choices=(
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ),
    default='PENDING'
)

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mail =models.EmailField(max_length=255,blank=True,null=True)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='COD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    razorpay_order_id = models.CharField(
        max_length=100, blank=True, null=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user}"

# ====================order item================

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.CharField(max_length=10, null=True, blank=True)


    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# ============ ORDER TRACKING ============
class Delivery(models.Model):
    # orders = Delivery.objects.filter(order__user=request.user).order_by('-order__created_at')
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    tracking_id = models.CharField(max_length=50, blank=True, null=True)    
    delivery_date = models.DateField(blank=True, null=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Delivery for Order {self.order.id}"
