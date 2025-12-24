# from django.conf import settings
# from django.core.mail import EmailMessage
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Order

# @receiver(post_save, sender=Order)
# def send_order_notification(sender, instance, created, **kwargs):
#     if not created:
#         return

#     try:
#         subject = f"New Order #{instance.id}"
#         body = f"""
# New Order Placed

# Order ID: {instance.id}
# User: {instance.user}
# Amount: ₹{instance.total_amount}
# Payment Method: {instance.payment_method}
# Status: {instance.status}
#         """

#         email = EmailMessage(
#             subject=subject,
#             body=body,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[settings.ADMIN_EMAIL],
#         )

#         email.send(fail_silently=True)  # 🔥 NEVER crash checkout

#     except Exception as e:
#         print("Order email error:", e)
