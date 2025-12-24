from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from products.models import Products
from users.models import UserAddress
from orders.models import Order, OrderItem,Delivery
# import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings



  
@login_required
def select_address(request):
    if request.method == "POST":
        address_id = request.POST['address_id']
        payment_method = request.POST['payment_method']
        return redirect(f"/payment/{address_id}/?method={payment_method}")

    addresses = UserAddress.objects.filter(user=request.user)
    return render(request, 'select_address.html', {"addresses": addresses})



@login_required
def save_address_and_payment(request, address_id):

    payment_method = request.GET.get('method', 'COD')
    selected_address = UserAddress.objects.get(id=address_id)

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


# order details
@login_required
def order_list(request):
    # Get all Delivery objects where the related Order belongs to the current user
    orders = Delivery.objects.filter(order__user=request.user).order_by('-order__created_at')
    return render(request, 'order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Delivery, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})










