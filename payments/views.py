import razorpay
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import UserAddress
from orders.models import Order
from cart.models import Cart
import requests
from django.http import JsonResponse
from products.models import Products
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

# q

# ===============================================================================================

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
# trails just =======================

@login_required
def checkout(request):
    addresses = UserAddress.objects.filter(user=request.user)


    delivery_charge = 199
    is_india = True


    # 🔴 ADDED: CLEAR BUY NOW SESSION WHEN USER COMES FROM CART CHECKOUT
    if request.GET.get('mode') == 'cart':
        request.session['buy_now'] = False
        request.session.pop('buy_now_item', None)

    # ---------------- BUY NOW MODE ----------------
    if request.session.get('buy_now'):

        buy_item = request.session.get('buy_now_item')
        product = get_object_or_404(Products, id=buy_item['product_id'])
        quantity = buy_item['quantity']

        total_amount = (product.price * quantity) + delivery_charge


        # ---------- GET ----------
        if request.method == "GET":
            return render(request, "payments/checkout_order.html", {
                "addresses": addresses,
                "buy_now_product": product,
                "buy_now_qty": quantity,
                "delivery_charge": delivery_charge,   # 🔴 ADD
                "is_india": is_india,                 # 🔴 ADD
                "amount": total_amount,
                "is_buy_now": True
            })

        # ---------- POST ----------
        if request.method == "POST":
            address_id = request.POST.get("address_id")
            address = get_object_or_404(UserAddress, id=address_id, user=request.user)

            # 🔴 DELIVERY BASED ON COUNTRY
            if address.country.strip().lower() != 'india':
                delivery_charge = 1600
                is_india = False

            
            total_amount = (product.price * quantity) + delivery_charge

            order = Order.objects.create(
                user=request.user,
                address=address,
                total_amount=total_amount,
                payment_method="UPI",
                status="Pending"
            )

            razorpay_order = client.order.create({
                "amount": int(total_amount * 100),
                "currency": "INR",
                "payment_capture": 1
            })

            order.razorpay_order_id = razorpay_order["id"]
            order.save()

            return JsonResponse({
                "razorpay_order_id": razorpay_order["id"],
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount": int(total_amount * 100),
                "order_db_id": order.id
            })

    # ---------------- NORMAL CART MODE ----------------
    cart_items = Cart.objects.filter(user=request.user)

    

    if request.method == "GET":
        cart_total = sum(item.subtotal() for item in cart_items)

        total_amount = cart_total +delivery_charge

        return render(request, "payments/checkout_order.html", {
            "addresses": addresses,
            "cart_items": cart_items,
            "delivery_charge": delivery_charge,
            "is_india": is_india,
            "amount": total_amount,
            "is_buy_now": False
        })

    if request.method == "POST":

        if not cart_items.exists():
            return JsonResponse({"error": "Cart is empty"}, status=400)

        address_id = request.POST.get("address_id")
        address = get_object_or_404(UserAddress, id=address_id, user=request.user)



        # 🔴 ADD THIS: DELIVERY CHARGE LOGIC
        if address.country.strip().lower() != 'india':
            delivery_charge = 1600
            is_india = False



        cart_total = sum(item.subtotal() for item in cart_items)
        total_amount = cart_total + delivery_charge

        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amount=total_amount,
            payment_method="UPI",
            status="Pending"
        )

        razorpay_order = client.order.create({
            "amount": int(total_amount * 100),
            "currency": "INR",
            "payment_capture": 1
        })

        order.razorpay_order_id = razorpay_order["id"]
        order.save()

        return JsonResponse({
            "razorpay_order_id": razorpay_order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": int(total_amount * 100),
            "order_db_id": order.id
        })



# buy_now_chekout=========================================
@login_required
def buy_now_checkout(request, id):
    product = get_object_or_404(Products, id=id)
    
    # Store Buy Now item in session
    request.session['buy_now_item'] = {
        'product_id': product.id,
        'quantity': 1
    }
    request.session['buy_now'] = True  # ✅ Add a flag

    return redirect('checkout')



# =================payment success view ==========================

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        params_dict = {
            "razorpay_payment_id": payment_id,
            "razorpay_order_id": razorpay_order_id,
            "razorpay_signature": signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.payment_status = "PAID"
            order.status = "Confirmed"
            order.save()

            # ✅ SEND ORDER DETAILS TO ADMIN ONLY
            # 🔥 ADMIN NOTIFICATIONS
            send_admin_order_mail(order)
            send_invoice_mail(order)
            send_whatsapp_alert(order)

            return redirect("order_success")

        except razorpay.errors.SignatureVerificationError:
            return render(request, "payments/failure.html")


# =======================send mail to admin ============================

# from django.core.mail import send_mail/
# from django.conf import settings

def send_admin_order_mail(order):
    subject = f"🧾 New Order Received | Order #{order.id}"

    message = f"""
NEW ORDER RECEIVED

Order ID: {order.id}
Customer: {order.user.username}
Phone: {order.address.phone}

Delivery Address:
{order.address}

---------------------------------
ORDER ITEMS
---------------------------------
"""

    for item in order.items.all():
        message += f"""
{item.product.name}
Qty: {item.quantity}
Price: ₹{item.price}
Subtotal: ₹{item.quantity * item.price}
---------------------------------
"""

    message += f"""
TOTAL AMOUNT: ₹{order.total_amount}

Payment Method: Razorpay
Payment Status: PAID

Andhra Sweets
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],  # ✅ ONLY YOUR MAIL
        fail_silently=False,
    )




# ===============invoice pdf  generated  ================
def generate_invoice_pdf(order):
    file_path = os.path.join(settings.MEDIA_ROOT, f"invoice_{order.id}.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "ANDHRA SWEETS - INVOICE")

    c.setFont("Helvetica", 10)
    c.drawString(50, 770, f"Order ID: {order.id}")
    c.drawString(50, 755, f"Customer: {order.user.username}")
    c.drawString(50, 740, f"Total Amount: ₹{order.total_amount}")

    y = 700
    c.drawString(50, y, "Items:")
    y -= 20

    for item in order.items.all():
        c.drawString(50, y, f"{item.product.name} × {item.quantity} = ₹{item.price * item.quantity}")
        y -= 15

    c.drawString(50, y - 10, f"TOTAL: ₹{order.total_amount}")
    c.save()

    return file_path
# mail invoice pdf to admin ========================

from django.core.mail import EmailMessage

def send_invoice_mail(order):
    pdf_path = generate_invoice_pdf(order)

    email = EmailMessage(
        subject=f"Invoice | Order #{order.id}",
        body="Invoice attached for the new order.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ADMIN_EMAIL],
    )

    email.attach_file(pdf_path)
    email.send()


# ================whats app poppup========================
# import requests

def send_whatsapp_alert(order):
    message = f"""
New Order Received
Order ID: {order.id}
Amount: ₹{order.total_amount}
Customer: {order.user.username}
"""

    url = "https://www.fast2sms.com/dev/whatsapp"
    headers = {
        "authorization": settings.FAST2SMS_API_KEY
    }

    payload = {
        "numbers": "6300100420",  # your WhatsApp number
        "message": message
    }

    requests.post(url, headers=headers, data=payload)


# get delivery charges==============================
@login_required
def get_delivery_charge(request):
    address_id = request.GET.get("address_id")
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)

    if address.country.strip().lower() == "india":
        return JsonResponse({
            "is_india": True,
            "delivery_charge": 199
        })
    else:
        return JsonResponse({
            "is_india": False,
            "delivery_charge": 1600
        })

