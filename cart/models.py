from django.db import models
from django.conf import settings
from products.models import Products

class Cart(models.Model):
    WEIGHT_CHOICES = (
        ("250", "250 gm"),
        ("500", "500 gm"),
        ("1000", "1 Kg"),
    )

    # ✅ Use custom user model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    # ❗ Your previous line was cut: `def`
    weight = models.CharField(max_length=10, choices=WEIGHT_CHOICES, default="250")


    #✅ Added field for customer requirements
    customer_req = models.TextField(blank=True, null=True, help_text="Special instructions like extra sugar, more spice, etc.")


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
