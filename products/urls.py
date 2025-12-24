from django.urls import path
from .views import home,pickles,sweets,dry_fruits,savories,podis,about,contact,product_detail,privacy,terms_conditions,delivery_policy,refund_return


urlpatterns =[
    path('', home, name='home'),
    # Categories
    path('sweets/', sweets, name='sweets'),
    path('pickles/', pickles, name='pickles'),
    path('dry-fruits/', dry_fruits, name='dry_fruits'),
    path('savories/', savories, name='savories'),
    path('masalas-podis/', podis, name='masalas_podis'),
    # Static Pages
    path('privacy', privacy, name='privacy'),
    path('terms/', terms_conditions, name='terms_conditions'),
    path('refund_return/', refund_return, name='refund_return'),
    path('delivery_policy/', delivery_policy, name='delivery_policy'),
    path('about/', about, name='about'),
    # path('blog/', blog, name='blog'),
    # path('<slug:slug>/',blog_detail, name='blog_detail'),
    path('contact/', contact, name='contact'),
    # Product Detail
    path('product/<int:id>/', product_detail, name='product_detail'),
]
