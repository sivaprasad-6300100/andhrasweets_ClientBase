from django.db import models
from django.contrib.auth.models import User
from products.models import Products
from users.models import Address


class Order(models.Model):

    PAYMENT_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('PHONEPE', 'PhonePe'),
        ('GPAY', 'Google Pay'),
        ('UPI', 'UPI'),
        ('PAYTM', 'Paytm'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='COD')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order} - {self.product}"
