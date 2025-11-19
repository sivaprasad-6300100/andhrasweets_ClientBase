from django.urls import path
from .views import checkout_view, ordersuccess_view


urlpatterns =[
    path('checkout/',checkout_view,name='checkout'),
    path('success/',ordersuccess_view,name='order_success'),
]