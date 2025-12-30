import razorpay
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import UserAddress
from orders.models import Order,OrderItem,Delivery
from cart.models import Cart
import requests
from datetime import datetime
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
from django.http import JsonResponse
from products.models import Products
from django.core.mail import EmailMessage

from django.utils import timezone
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


# ✅ NORTH INDIA STATES
NORTH_INDIA_STATES = [
    "delhi", "haryana", "punjab", "uttar pradesh",
    "uttarakhand", "himachal pradesh", "rajasthan",
    "chandigarh", "jammu and kashmir", "ladakh"
]
# trails just =======================

@login_required
def checkout(request):
    addresses = UserAddress.objects.filter(user=request.user)


    delivery_charge =  0   # 🇮🇳 FREE delivery
    is_india = True

    # 🔴 ADDED: CLEAR BUY NOW SESSION WHEN USER COMES FROM CART CHECKOUT 
    if request.GET.get('mode') == 'cart':
        request.session['buy_now'] = False
        request.session.pop('buy_now_item', None)

    # ---------------- BUY NOW MODE ----------------
    if request.session.get('buy_now'):

        buy_item = request.session.get('buy_now_item')
        product = get_object_or_404(Products, id=buy_item['product_id'])

        price = buy_item['price']
        quantity = buy_item['quantity']
        weight = buy_item['weight']

        base_amount = price * quantity
        total_amount = base_amount + delivery_charge


        # ---------- GET ----------
        if request.method == "GET":
            return render(request, "payments/checkout_order.html", {
                "addresses": addresses,
                "buy_now_product": product,
                "buy_now_qty": quantity,
                "buy_now_price": price,          # ✅ PASS PRICE
                "buy_now_weight": weight,  
                "delivery_charge": delivery_charge,   # 🔴 ADD
                "is_india": is_india,                 # 🔴 ADD
                "amount": total_amount,
                "base_amount": base_amount,   # ✅ ADD THIS
                "is_buy_now": True
            })

        # ---------- POST ----------
        if request.method == "POST":
            address_id = request.POST.get("address_id")
            address = get_object_or_404(UserAddress, id=address_id, user=request.user)

            country = address.country.strip().lower()
            state = address.state_province.strip().lower()

            # 🔴 DELIVERY BASED ON COUNTRY
            if country != "india":
                delivery_charge = 1600
                is_india = False
            elif state in NORTH_INDIA_STATES:
                delivery_charge = 100
                is_india = True
            else:
                delivery_charge = 0
                is_india = True
            
            
            base_amount = price * quantity
            total_amount = base_amount + delivery_charge

            order = Order.objects.create(
                user=request.user,
                address=address,
                total_amount=total_amount,
                subtotal=base_amount,
                delivery_charge=delivery_charge,
                payment_method="UPI",
                status="Pending"
            )

            # ✅ SAVE BUY NOW ITEM (ONLY ONE PRODUCT)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
                weight=weight
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

    # ---------------- CART MODE ----------------
    cart_items = Cart.objects.filter(user=request.user)

    

    if request.method == "GET":
        base_amount= sum(item.subtotal() for item in cart_items)

        total_amount = base_amount +delivery_charge

        return render(request, "payments/checkout_order.html", {
            "addresses": addresses,
            "cart_items": cart_items,
            "delivery_charge": delivery_charge,
            "is_india": is_india,
            "amount": total_amount,
            "base_amount": base_amount,
            "is_buy_now": False
        })

    if request.method == "POST":

        if not cart_items.exists():
            return JsonResponse({"error": "Cart is empty"}, status=400)

        address_id = request.POST.get("address_id")
        address = get_object_or_404(UserAddress, id=address_id, user=request.user)



        country = address.country.strip().lower()
        state = address.state_province.strip().lower()


        # ✅ DELIVERY CHARGE LOGIC
        if country != "india":
            delivery_charge = 1600
            is_india = False
        elif state in NORTH_INDIA_STATES:
            delivery_charge = 100
            is_india = True
        else:
            delivery_charge = 0
            is_india = True


        cart_total = sum(item.subtotal() for item in cart_items)
        total_amount = cart_total + delivery_charge

        order = Order.objects.create(
            user=request.user,
            address=address,
            subtotal=cart_total,
            delivery_charge=delivery_charge,
            total_amount=total_amount,
            payment_method="ONLINE",
            status="Pending"
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.get_price(),   # ✅ CORRECT PRICE BY WEIGHT
                weight=item.weight        # ✅ CORRECT WEIGHT
            
                
            )
            # ✅ CLEAR CART AFTER SAVING
        cart_items.delete()


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
    if request.method != "POST":
        return redirect('product_detail', id=id)

    product = get_object_or_404(Products, id=id)

    # 🔥 READ DATA FROM FORM
    weight = request.POST.get('weight', '250')
    quantity = int(request.POST.get('quantity', 1))

    # 🔥 PRICE BY WEIGHT
    if weight == '250':
        price = product.price_250
    elif weight == '500':
        price = product.price_500
    elif weight == '1000':
        price = product.price_1000
    else:
        price = product.price_250

    # 🔥 SAVE EVERYTHING IN SESSION
    request.session['buy_now_item'] = {
        'product_id': product.id,
        'quantity': quantity,
        'weight': weight,
        'price': float(price)
    }
    request.session['buy_now'] = True

    return redirect('checkout')


# =================payment success view ==========================

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        return redirect("order_success")


# =======================send mail to admin ============================

# from django.core.mail import send_mail/
# from django.conf import settings

def send_admin_order_mail_with_pdf(order,pdf_path_seller):
    subject = f"🧾 New Order Received | Order #{order.id}"

    message = f"""
📦 NEW ORDER RECEIVED – ACTION REQUIRED

Dear Admin,

A new order has been successfully placed on Andhrasruchulu.

Order Details:
• Order ID   : {order.id}
• Customer   : {order.user.name}

Please review the order and proceed with the next steps at the earliest.

Regards,
Andhrasruchulu System
"""

    email =EmailMessage(
        subject=subject,
        body=message,
        from_email =settings.EMAIL_HOST_USER,
        to=[settings.ADMIN_EMAIL]
    )

    email.attach_file(pdf_path_seller)

    email.send(fail_silently=False)


# generate invoice for seller =========================



def generate_invoice_seller_pdf(order):
    # File path
    invoice_name = f"invoice_order_{order.id}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, invoice_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # ================= COMPANY HEADER =================
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "ANDHRASRUCHULU")

    c.setFont("Helvetica", 9)
    c.drawString(50, height - 70, "www.andhrasruchulu.com")
    c.drawString(50, height - 85, "Email: andhrasweetsandpickles@gmail.com")
    c.drawString(50, height - 100, "Phone: +91-9490128341")
    c.drawString(50, height - 115, "Andhra Pradesh – 524004")

    # ================= INVOICE DETAILS (RIGHT) =================
    c.setFont("Helvetica", 10)
    c.drawString(350, height - 70, f"Invoice No: INV-{order.id}")
    c.drawString(350, height - 85, f"Order ID: {order.id}")
    c.drawString(350, height - 100, f"Invoice Date: {datetime.now().strftime('%d-%m-%Y')}")
    c.drawString(350, height - 115, "Payment Method: Razorpay")
    c.drawString(350, height - 130, "Payment Status: PAID")

    # ================= LINE =================
    c.line(50, height - 150, width - 50, height - 150)


    # ================= CUSTOMER DETAILS =================
    y = height - 180
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "BILL TO")

    y -= 18
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Name: {order.user.name}")

    y -= 15
    c.drawString(50, y, f"Phone: {order.user.phone}")

    y -= 18
    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "Delivery Address:")

    y -= 14
    c.setFont("Helvetica", 9)

    text = c.beginText(50, y)
    for line in str(order.address).split(","):
        text.textLine(line.strip())
        y -= 12

    c.drawText(text)


    # ================= ITEMS TABLE HEADER =================

    # ================= ITEMS TABLE =================
    y -= 25
    c.line(50, y, width - 50, y)

    y -= 18
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Product")
    c.drawString(220, y, "Weight")
    c.drawString(280, y, "Qty")
    c.drawString(330, y, "Price")
    c.drawString(420, y, "Total")

    y -= 8
    c.line(50, y, width - 50, y)

    # ================= ITEMS =================
    c.setFont("Helvetica", 10)
    y -= 20

    for item in order.items.all():
        c.drawString(50, y, item.product.name)
        c.drawString(220, y, f"{item.weight} g")  # ✅ ADD
        c.drawString(280, y, str(item.quantity))
        c.drawString(330, y, f"₹ {item.price}")
        c.drawString(420, y, f"₹ {item.price * item.quantity}")
        y -= 18

    # ================= TOTALS =================

    y -= 10
    c.line(300, y, width - 50, y)

    y -= 16
    c.setFont("Helvetica", 10)
    c.drawString(330, y, "Subtotal:")
    c.drawRightString(width - 50, y, f"₹ {order.subtotal:.2f}")

    y -= 14
    c.drawString(330, y, "Delivery Charges:")
    c.drawRightString(width - 50, y, f"₹ {order.delivery_charge:.2f}")

    y -= 18
    c.setFont("Helvetica-Bold", 11)
    c.drawString(330, y, "GRAND TOTAL:")
    c.drawRightString(width - 50, y, f"₹ {order.total_amount:.2f}")

    # ================= FOOTER =================
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 80, "Thank you for your business with Andhrasruchulu.")
    c.drawString(50, 65, "This is a computer-generated invoice.")

    # Save PDF
    c.save()

    return file_path



# ===============invoice pdf  generated  ================

def generate_invoice_pdf(order):
    file_path = os.path.join(settings.MEDIA_ROOT, f"invoice_{order.id}.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)

    # ================= HEADER =================
    y = 800
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "andhrasruchulu_Order - INVOICE")

    y -= 25
    c.setFont("Helvetica", 9)
    c.drawString(50, y, "andhrasruchulu.com")

    y -= 15
    c.drawString(50, y, "Andhra Pradesh - 524004")


    y -= 15
    c.drawString(50, y, "Phone: +91-9490128341")

    y -= 15
    c.drawString(50, y, "Email: andhrasweetsandpickles@gmail.com")

    # ================= ORDER & CUSTOMER DETAILS =================
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Order ID: {order.id}")

    y -= 15
    c.drawString(50, y, f"Customer Name: {order.user.name}")

    y -= 15
    c.drawString(50, y, f"Customer Phone: {order.user.phone}")

    # Right side invoice info
    c.drawString(350, y + 30, f"Invoice Date: {datetime.now().strftime('%d-%m-%Y')}")
    c.drawString(350, y + 15, "Payment Method: Razorpay")
    c.drawString(350, y, "Payment Status: Paid")

    # ================= SEPARATOR =================
    y -= 25
    c.line(50, y, 550, y)

    # ================= ITEMS TABLE HEADER =================
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Product")
    c.drawString(220, y, "Weight")   # ✅
    c.drawString(280, y, "Qty")
    c.drawString(330, y, "Price")
    c.drawString(420, y, "Total")

    y -= 10
    c.line(50, y, 550, y)

    # ================= ITEMS LIST =================
    y -= 15
    c.setFont("Helvetica", 10)

    for item in order.items.all():
        c.drawString(50, y, item.product.name)
        c.drawString(220, y, f"{item.weight} g")  # ✅ ADD
        c.drawString(280, y, str(item.quantity))
        c.drawString(330, y, f"Rs {item.price}")
        c.drawString(420, y, f"Rs {item.price * item.quantity}")
        y -= 15

    # ================= TOTALS =================
    y -= 10
    c.line(300, y, 550, y)

    y -= 15
    c.drawString(330, y, "Subtotal:")
    items_total = sum(
    item.price * item.quantity
    for item in order.items.all()
    )

    c.drawString(420, y, f"Rs {items_total}")


    y -= 15
    c.drawString(330, y, "Delivery Charges:")
    c.drawString(420, y, f"Rs {order.delivery_charge}")

    y -= 15
    c.setFont("Helvetica-Bold", 10)
    c.drawString(330, y, "Grand Total:")
    c.drawString(420, y, f"Rs {order.total_amount}")

    # ================= FOOTER =================
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 100, "Thank you for shopping with Andhrasruchulu!")
    c.drawString(50, 85, "This is a computer-generated invoice.")

    c.save()
    return file_path

# mail invoice pdf to admin ========================


def send_invoice_email(order, pdf_path):
    subject = f"Your Invoice - Order #{order.id}"
    message = f"""
Dear {order.user.name},

Thank you for shopping with Andhras Ruchulu ❤️

Please find your invoice attached.

Order ID: {order.id}
Amount Paid: Rs {order.total_amount}

Regards,
Andhras Ruchulu Team
"""

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[order.address.mail],   # CUSTOMER EMAIL
    )

    # ✅ Attach PDF
    email.attach_file(pdf_path)
    

    email.send(fail_silently=False)

    



# ================whats app poppup========================
# import requests

def send_whatsapp_alert(order):
    message = f"""
New Order Received
Order ID: {order.id}
Amount: Rs{order.total_amount}
Customer: {order.user.phone}
"""

    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        "authorization": settings.FAST2SMS_API_KEY
    }

    payload = {
        "route": "q",
        "numbers": "9490128341",  # your WhatsApp number
        "message": message
    }

    requests.post(url, headers=headers, data=payload)


# get delivery charges=============================

@login_required
def get_delivery_charge(request):
    address_id = request.GET.get("address_id")
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)

    country = address.country.strip().lower()
    state = address.state_province.strip().lower()  # ✅ SAME FIELD AS TEMPLATE

    # 🌍 OUTSIDE INDIA
    if country != "india":
        return JsonResponse({
            "country": country,
            "delivery_charge": 1600
        })

    # 🇮🇳 INDIA → NORTH INDIA
    if state in NORTH_INDIA_STATES:
        return JsonResponse({
            "country": "india",
            "delivery_charge": 100
        })

    # 🇮🇳 INDIA → OTHER STATES (FREE)
    return JsonResponse({
        "country": "india",
        "delivery_charge": 0
    })


# order succss view ========================
def order_success(request):
    return render(request, "payments/success.html")


# order details===============


# payment webhooks=========================
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
import json




@csrf_exempt
def razorpay_webhook(request):
    if request.method == "POST":
        payload = request.body
        signature = request.headers.get("X-Razorpay-Signature")

        try:
            client.utility.verify_webhook_signature(
                payload,
                signature,
                settings.RAZORPAY_WEBHOOK_SECRET
            )
        except razorpay.errors.SignatureVerificationError:
            return HttpResponse(status=400)

        data = json.loads(payload)
        event = data.get("event")

        # ✅ ONLY HANDLE PAYMENT CAPTURED
        if event == "payment.captured":
            payment = data["payload"]["payment"]["entity"]
            razorpay_order_id = payment["order_id"]

            try:
                order = Order.objects.get(razorpay_order_id=razorpay_order_id)

                # 🔒 Avoid duplicate execution
                if order.payment_status != "PAID":
                    order.payment_status = "PAID"
                    order.status = "Confirmed"
                    order.save()

                    # 🔥 SEND MAILS & WHATSAPP HERE (SAFE)
                    pdf_path_seller = generate_invoice_seller_pdf(order)
                    send_admin_order_mail_with_pdf(order, pdf_path_seller)

                    pdf_path = generate_invoice_pdf(order)
                    send_invoice_email(order, pdf_path)

                    send_whatsapp_alert(order)

            except Order.DoesNotExist:
                pass

        return HttpResponse(status=200)