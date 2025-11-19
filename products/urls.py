from django.urls import path
from .views import home,pickles,sweets,dry_fruits,savories,masalas_podis,about,blog,contact,product_detail


urlpatterns =[
    path('', home, name='home'),
    # Categories
    path('sweets/', sweets, name='sweets'),
    path('pickles/', pickles, name='pickles'),
    path('dry-fruits/', dry_fruits, name='dry_fruits'),
    path('savories/', savories, name='savories'),
    path('masalas-podis/', masalas_podis, name='masalas_podis'),
    # Static Pages
    path('about/', about, name='about'),
    path('blog/', blog, name='blog'),
    path('contact/', contact, name='contact'),
    # Product Detail
    path('product/<int:id>/', product_detail, name='product_detail'),
]
