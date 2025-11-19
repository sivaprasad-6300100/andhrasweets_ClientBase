from django.shortcuts import render

# Create your views here.

def checkout_view(request):
    return render(request,'order/checkout.html')

def ordersuccess_view(request):
    return render(request,'order/order_success.html')
