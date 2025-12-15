from django.urls import path
from users.views import add_address,address_list,edit_address,delete_address,register_view,login_phone_view,otp_verify_view,logout_view,fake_view

urlpatterns = [
    path('addresses/',address_list, name="address_list"),
    path('addresses/add/',add_address, name="add_address"),
    path('addresses/<int:id>/edit/',edit_address, name="edit_address"),
    path('addresses/<int:id>/delete/',delete_address, name="delete_address"),

    # ========register urls=============
    path('register_view/',register_view,name='user_register'),
    path('login_phone_view/',login_phone_view,name='login_phone_view'),
    path('otp_verify/',otp_verify_view,name='otp_verify'),
    path('logout_view/',logout_view,name='logout'),
    path('fake_view/',fake_view,name='fake_view')

    
]
