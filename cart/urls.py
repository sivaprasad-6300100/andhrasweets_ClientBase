from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/buy/', views.buy_now, name='buy_now'),
    path('<int:id>/add/', views.add_to_cart, name='add_to_cart'),
    path('cart_page/',views.cart_page,name='cart_page'),
    path('cart/delete/<int:cart_id>/', views.delete_cart_item, name='delete_cart_item'),

]
