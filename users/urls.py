from django.urls import path
from users.views import add_address,address_list,edit_address,delete_address

urlpatterns = [
    path('addresses/',address_list, name="address_list"),
    path('addresses/add/',add_address, name="add_address"),
    path('addresses/<int:id>/edit/',edit_address, name="edit_address"),
    path('addresses/<int:id>/delete/',delete_address, name="delete_address"),
]
