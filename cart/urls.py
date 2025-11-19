from django.urls import path
from .views import cart_view,empty_cart


urlpatterns =[
    path('',cart_view,name='cart'),
    path('empty/',empty_cart,name='empty_cart'),
]