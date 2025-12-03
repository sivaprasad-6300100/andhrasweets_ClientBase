from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserProfileForm, VerifyOTPForm
from .models import UserProfile,Cart
from django.contrib import messages
from products.models import Products
from orders.models import Order,OrderItem
from users.models import Address
from cart.models import Cart




def user_register(request):
    # registration form
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            # TODO: Replace print with SMS API (Twilio, Fast2SMS, MSG91)
            print(f"DEBUG: OTP for {user.phone} is {user.otp}")  # for testing only

            # save user id to session so verify view knows which user
            request.session['otp_user_id'] = user.id
            # optional: set session expiry for OTP lifetime (e.g., 5 minutes)
            # request.session.set_expiry(300)

            messages.success(request, f"OTP sent to {user.phone}")
            return redirect('verify_otp')
    else:
        form = UserProfileForm()
    return render(request, 'login_phone.html', {'form': form})


def verify_otp(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, "No OTP session found. Please register first.")
        return redirect('user_register')

    user = get_object_or_404(UserProfile, id=user_id)
    if request.method == "POST":
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp_submitted = form.cleaned_data['otp']
            if user.otp == otp_submitted:
                user.is_verified = True
                user.otp = ''  # clear OTP after success (optional)
                user.save()
                # clear session
                try:
                    del request.session['otp_user_id']
                except KeyError:
                    pass
                messages.success(request, "Phone verified successfully!")
                return redirect('verification_success')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
    else:
        form = VerifyOTPForm()
    return render(request, 'verify_otp.html', {'form': form, 'phone': user.phone})


def verification_success(request):
    return render(request, 'verification_success.html')


# def cart_view(request):
    # return render(request,'cart.html')



# def empty_cart(request):
    # return render(request,'empty_cart.html')


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Products, id=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('cart_page')


@login_required
def buy_now(request, id):
    product = get_object_or_404(Products, id=id)
    request.session['buy_now_product'] = product.id
    return redirect('select_address')


@login_required
def cart_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in cart_items)
    return render(request, 'cart.html', {"cart_items": cart_items, "total": total})


def delete_cart_item(request, cart_id):
    # Ensure only the owner can delete
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart_page')  # Redirect back to the cart page