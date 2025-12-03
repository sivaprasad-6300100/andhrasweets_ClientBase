from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('verified/', views.verification_success, name='verification_success'),
    path('<int:id>/buy/', views.buy_now, name='buy_now'),
    path('<int:id>/add/', views.add_to_cart, name='add_to_cart'),
    path('cart_page',views.cart_page,name='cart_page'),
    path('cart/delete/<int:cart_id>/', views.delete_cart_item, name='delete_cart_item'),

]
