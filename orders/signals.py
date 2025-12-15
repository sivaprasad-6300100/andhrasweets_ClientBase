from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, OrderItem


@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    if created:

        # ------------- GET ORDER ITEMS ----------------
        items = OrderItem.objects.filter(order=instance)

        items_text = ""
        for item in items:
            gram_info = ""
            if hasattr(item.product, 'grams'):
                gram_info = f" ({item.product.grams}g)"

            items_text += (
                f"- {item.product.name}{gram_info} | Qty: {item.quantity} | Price: ₹{item.price}\n"
            )

        # ------------- FULL EMAIL MESSAGE -------------
        subject = f"New Order Received - #{instance.id}"

        message = f"""
A new order has been placed on your website.

===============================
        CUSTOMER DETAILS
===============================
User ID: {instance.user.id}
User Name: {instance.user.username}
Phone: {instance.address.phone_number}

===============================
           ADDRESS
===============================
{instance.address.full_name}
{instance.address.address_line_1}
{instance.address.city}, {instance.address.state} - {instance.address.pincode}

===============================
          ORDER ITEMS
===============================
{items_text}

===============================
         ORDER SUMMARY
===============================
Total Amount: ₹{instance.total_amount}
Payment Method: {instance.payment_method}
Status: {instance.status}
Created At: {instance.created_at.strftime('%d-%m-%Y %H:%M')}
Order ID: {instance.id}

Login to your admin panel to view full details.
"""

        # ----------- SEND EMAIL ----------------
        send_mail(
            'Test Email',
            'This is a test email body',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
