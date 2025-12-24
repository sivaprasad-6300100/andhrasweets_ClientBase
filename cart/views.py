from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from products.models import Products
from django.conf import settings
# from orders.models import Order, OrderItem
# from users.models import UserAddress
from cart.models import Cart  # single authoritative Cart import



@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Products, id=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('cart_page')





@login_required
def cart_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in cart_items)
    return render(request, 'cart.html', {"cart_items": cart_items, "total": total})


@login_required
def delete_cart_item(request, cart_id):
    # Ensure only the owner can delete - this will 404 if user doesn't own the cart item
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart_page')
