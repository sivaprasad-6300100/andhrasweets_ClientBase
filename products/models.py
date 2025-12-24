from django.db import models


class Products(models.Model):
    CATEGORY_CHOICES = (
        ("veg-pickles", "Veg Pickles"),
        ("nonveg-pickles", "Non-Veg Pickles"),
        ("sweets", "Sweets"),
        ("podis", "Podis"),
        ("savories", "Savories"),
        ("dry-fruits", "Dry Fruits"),
    )

    name = models.CharField(max_length=200)
    telugu_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)


     # New weight–based prices
    price_250 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    price_500 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    price_1000 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  # 1kg

    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.name
    


class Banner(models.Model):
    PAGE_CHOICES =(
        ("pickles","pickles page"),
        ("sweets","sweets page"),
        ("savories","savories page"),
        ("masalas","masalas page"),
        ("dryfruits","dryfruits page"),
        ("home","home page"),
    )


    page  =models.CharField(max_length=50,choices=PAGE_CHOICES,unique=True)
    images =models.ImageField(upload_to="banners/")
    alt_text =models.CharField(max_length=200, blank=True)


    def __str__(self):
        return f"{self.page} Banner"
    


    # Blog Model============================

    # from django.db import models

# class Blog_Model(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True)
#     image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_published = models.BooleanField(default=True)

#     def __str__(self):
#         return self.title

