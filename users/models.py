from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    address = models.TextField()
    landmark = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} - {self.address}"
