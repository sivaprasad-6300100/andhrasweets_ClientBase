# reviews/models.py
from django.db import models
from users.models import UserProfile
from products.models import Products

class Review_Model(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rating = models.IntegerField()  # 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")  # 🔐 prevent spam

    def __str__(self):
            return f"{self.product.name} - {self.rating}⭐"
