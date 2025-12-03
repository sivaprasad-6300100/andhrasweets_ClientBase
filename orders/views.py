from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from products.models import Products
from users.models import Address
from orders.models import Order, OrderItem

@login_required
def select_address(request):
    if request.method == "POST":
        address_id = request.POST['address_id']
        payment_method = request.POST['payment_method']
        return redirect(f"/payment/{address_id}/?method={payment_method}")

    addresses = Address.objects.filter(user=request.user)
    return render(request, 'select_address.html', {"addresses": addresses})



@login_required
def save_address_and_payment(request, address_id):

    payment_method = request.GET.get('method', 'COD')
    selected_address = Address.objects.get(id=address_id)

    # BUY NOW FLOW
    if 'buy_now_product' in request.session:
        product_id = request.session['buy_now_product']
        product = Products.objects.get(id=product_id)
        total = product.price

        order = Order.objects.create(
            user=request.user,
            address=selected_address,
            total_amount=total,
            payment_method=payment_method
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1
        )
        del request.session['buy_now_product']
        return redirect('order_success')

    # CART CHECKOUT FLOW
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        address=selected_address,
        total_amount=total,
        payment_method=payment_method
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    cart_items.delete()
    return redirect('order_success')


@login_required
def order_success(request):
    return render(request, 'success.html')
