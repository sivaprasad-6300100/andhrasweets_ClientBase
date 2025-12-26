from django.urls import path
from . import views



urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('checkout/success/',views.payment_success,name='payment_success'),
    path('checkout_page/<int:id>/',views.buy_now_checkout,name='buy_now_checkout'),
    path("get-delivery-charge/", views.get_delivery_charge, name="get_delivery_charge"),

]
