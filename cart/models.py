from django.db import models
from django.utils import timezone
from products.models import Products
from django.contrib.auth.models import User



class UserProfile(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"
    
class Cart(models.Model):
    WEIGHT_CHOICES = (
        ("250", "250 gm"),
        ("500", "500 gm"),
        ("1000", "1 Kg"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    weight = models.CharField(max_length=10, choices=WEIGHT_CHOICES, default="500")  # NEW FIELD

    def get_price(self):
        """Return price based on selected weight."""
        if self.weight == "250":
            return self.product.price_250 or 0
        elif self.weight == "500":
            return self.product.price_500 or 0
        elif self.weight == "1000":
            return self.product.price_1000 or 0
        return 0

    def subtotal(self):
        """subtotal = selected weight price × quantity"""
        return self.get_price() * self.quantity

    def __str__(self):
        return f"{self.user} - {self.product} ({self.weight}g)"



