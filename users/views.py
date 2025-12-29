from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import UserAddress,UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
# from .models import UserProfile
from .forms import RegisterForm
import random
from .forms import OTPForm
# import requests


# =====================otp flow Fast2sms========================
# FAST2SMS_API_KEY = "CflRJgWb47q1LvmTi2Q6cADhn98uPBXt0xoj5SrpeHOUsMFzYIa1zRATCLv7QPN93rK5yoIZXi2jDWJx"

def send_fast2sms_otp(phone, otp):
    # TEMPORARY OTP – print to console
    print(f"[TEMP OTP] Phone: {phone}, OTP: {otp}")
    
    # Return fake success response like Fast2SMS
    return {"return": True, "message": "OTP printed to console"}


# address_list_view ==============================
@login_required
def address_list(request):
    # UPDATE address
    if request.method == "POST" and "update_id" in request.POST:
        address = get_object_or_404(
            UserAddress,
            id=request.POST.get("update_id"),
            user=request.user
        )
        address.full_name=request.POST.get('full_name')
        address.phone=request.POST.get('phone')
        address.mail =request.POST.get('mail')
        address.address_line1=request.POST.get('address_line1')
        address.address_line2=request.POST.get('address_line2')
        address.city=request.POST.get('city')
        address.state_province=request.POST.get('state_province')
        address.postal_code=request.POST.get('postal_code')
        address.country=request.POST.get('country')
        address.address_type=request.POST.get('address_type')
        address.save()
        
        return redirect("address_list")

    # DELETE address
    if request.method == "POST" and "delete_id" in request.POST:
        address = get_object_or_404(
            UserAddress,
            id=request.POST.get("delete_id"),
            user=request.user
        )
        address.delete()
        return redirect("address_list")

    addresses = UserAddress.objects.filter(user=request.user)
    return render(request, "address_list.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        UserAddress.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            mail =request.POST.get('mail'),
            address_line1=request.POST.get('address_line1'),
            address_line2=request.POST.get('address_line2'),
            city=request.POST.get('city'),
            state_province=request.POST.get('state_province'),
            postal_code=request.POST.get('postal_code'),
            country=request.POST.get('country'),
            address_type=request.POST.get('address_type'),
     )
        return redirect('address_list')
    return render(request, "add_address.html")

@login_required
def edit_address(request, id):
    address = get_object_or_404(UserAddress, id=id, user=request.user)

    if request.method == "POST":
        address.full_name = request.POST['full_name']
        address.phone = request.POST['phone']
        address.mail =request.POST['mail'],
        address.address_line1 = request.POST['address_line1']
        address.address_line2 = request.POST['address_line2']
        address.city = request.POST['city']
        address.state_province = request.POST['state_province']
        address.postal_code = request.POST['postal_code']
        address.country =request.POST['country']
        address.save()
        return redirect('address_list')

    return render(request, "edit_address.html", {"address": address})

@login_required
def delete_address(request, id):
    address = get_object_or_404(UserAddress, id=id, user=request.user)
    address.delete()
    return redirect('address_list')



# ==============================================
# user registration view=====================================

def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            phone = form.cleaned_data["phone"]
            name = form.cleaned_data["name"]

            user, created = UserProfile.objects.get_or_create(phone=phone)

            if not created and user.name:
                messages.error(request, "Phone already registered. Please login.")
                return redirect("user_register")

            user.name = name
            user.otp = "1234"

            user.save()

            # sms_response = send_fast2sms_otp(phone, user.otp)

            # if not sms_response.get("return"):
                # messages.error(request, "Failed to send OTP. Try again.")
                # return redirect("user_register")

            request.session["phone"] = phone
            messages.success(request, "Enter the for Testing Purpose 1234.")
            return redirect("otp_verify")

    return render(request, "login_phone.html", {"form": form})


# already existing view ====================

def login_phone_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone")

        if not UserProfile.objects.filter(phone=phone).exists():
            return render(request, "existing_user.html", {
                "error": "Phone not registered. Please register.",
                "phone": phone
            })

        user = UserProfile.objects.get(phone=phone)
        user.otp = "1234"
        user.save()

        # sms_response = send_fast2sms_otp(phone, user.otp)

        # if not sms_response.get("return"):
            # messages.error(request, "Failed to send OTP.")
            # return redirect("login_phone_view")

        request.session["phone"] = phone
        return redirect("otp_verify")

    return render(request, "existing_user.html")


# =======================
        #  vierify otp_verify_view
    # ==============================


def otp_verify_view(request):
    phone = request.session.get("phone")

    if not phone:
        messages.error(request, "Session expired. Please login again.")
        return redirect("user_register")

    try:
        user = UserProfile.objects.get(phone=phone)
    except UserProfile.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("user_register")
    

    
    # AUTO LOGIN WITHOUT FORM
    if user.otp == "1234":
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        user.otp = None
        user.save()
        return redirect("home")

    # Optional fallback if you still want manual OTP
    form = OTPForm()
    return render(request, "verify_otp.html", {"form": form})

    # form = OTPForm()

    # if request.method == "POST":
        # form = OTPForm(request.POST)
        # if form.is_valid():
            # otp_input = form.cleaned_data["otp"]

            # if otp_input == user.otp:
                # user.backend = 'django.contrib.auth.backends.ModelBackend'
                # login(request, user)

                # user.otp = None
                # user.save()

                # return redirect("home")
            # else:
                # messages.error(request, "Invalid OTP")

    # return render(request, "verify_otp.html", {"form": form})







def logout_view(request):
    # request.session.flush()   # 🔥 clears cart + session data
    logout(request)
    return redirect("home")


# def fake_view(request):
    # return render(request,'existing_user.html')
# 
 
 




# to checking whether the user is already loggeed or not

def check_phone(request):
    phone = request.GET.get("phone")
    exists = UserProfile.objects.filter(phone=phone).exists()
    return JsonResponse({"exists": exists})




# Blog page  views==========================

