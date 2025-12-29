from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.http import JsonResponse
from django.utils import timezone
# from django.utils.text import slugify


class UserProfileManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # auto timestamp
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # 🔥 IMPORTANT
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "phone"    
    REQUIRED_FIELDS = []  # No username or email

    def __str__(self):
        return self.phone





# =======================user address new model =========================
class UserAddress(models.Model):

    ADDRESS_TYPES = (
        ('Home', 'Home'),
        ('Office', 'Office'),
    )

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    mail =models.EmailField(max_length=255,blank=True,null=True)
    address_line1 = models.TextField()
    address_line2 = models.TextField()
    city = models.CharField(max_length=50)
    state_province = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

    country = models.CharField(
        max_length=50,
        default='India'
    )

    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPES,
        default='Home'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} ={self.full_name}, {self.phone},{self.address_line1}, {self.address_line2}, {self.city}, {self.state_province},{self.country},{self.postal_code}----{self.mail}"
























    


    




