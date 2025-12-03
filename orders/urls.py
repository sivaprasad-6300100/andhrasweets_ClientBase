from django.urls import path
from . import views

urlpatterns = [
    path('select_address/', views.select_address, name='select_address'),
    path('pay/<int:address_id>/', views.save_address_and_payment, name='payment'),
    path('success/', views.order_success, name='order_success'),
]
