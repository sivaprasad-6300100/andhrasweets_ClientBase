from django.urls import path
from . import views

app_name='orders'

urlpatterns = [
    path('select_address/', views.select_address, name='select_address'),
    path('pay/<int:address_id>/', views.save_address_and_payment, name='payment'),
    path('success/', views.order_success, name='order_success'),

    # order details===========
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]
