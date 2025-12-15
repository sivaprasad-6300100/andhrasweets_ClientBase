from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserAddress
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import UserProfile
from .forms import RegisterForm
import random
from .forms import OTPForm



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

# user registration view================
def register_view(request):

    form = RegisterForm()   # load the form

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            phone = form.cleaned_data["phone"]
            name = form.cleaned_data["name"]

            # Get or create user
            user, created = UserProfile.objects.get_or_create(phone=phone)

            # If phone already exists AND user has name → already registered
            if not created and user.name:
                messages.error(request, "Phone already registered. Please Login.")
                return redirect("user_register")

            # Save new user OR update name
            user.name = name

            # Generate OTP
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()

            # Store phone in session for OTP verification
            request.session["phone"] = phone

            messages.success(request, "OTP sent!")
            return redirect("otp_verify")

    # If GET → show form
    return render(request, "login_phone.html", {"form": form})



# already existing view ====================



def login_phone_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone")

        # ❌ Phone not registered
        if not UserProfile.objects.filter(phone=phone).exists():
            return render(request, "existing_user.html", {
                "error": "Phone not registered. Please register.",
                "phone": phone
            })

        # ✔ Phone exists → generate OTP
        user = UserProfile.objects.get(phone=phone)
        user.otp = str(random.randint(100000, 999999))
        user.save()

        print("OTP:", user.otp)  # Debug only

        # Save phone in session so OTP page can access it
        request.session["phone"] = phone

        # Redirect to OTP page without passing phone in URL
        return redirect("otp_verify")

    # GET → show form
    return render(request, "existing_user.html")


def fake_view(request):
    return render(request,'existing_user.html')

# =======================
        #  vierify otp_verify_view
    # ===============================

def otp_verify_view(request):
    phone = request.session.get("phone")  # get phone from session

    if not phone:
        messages.error(request, "Session expired. Please login again.")
        return redirect("user_register")

    try:
        user = UserProfile.objects.get(phone=phone)
    except UserProfile.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("user_register")

    form = OTPForm()

    print("OTP sent to user:", user.otp)   # SHOW OTP IN TERMINAL AGAIN

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_input = form.cleaned_data["otp"]

            if otp_input == user.otp:
                login(request, user)
                user.otp = None
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # ← Add this
                return redirect("home")
            else:
                messages.error(request, "Invalid OTP")

    return render(request, "verify_otp.html", {"form": form})



def logout_view(request):
    # request.session.flush()   # 🔥 clears cart + session data
    logout(request)
    return redirect("home")
 
 




# to checking whether the user is already loggeed or not

def check_phone(request):
    phone = request.GET.get("phone")
    exists = UserProfile.objects.filter(phone=phone).exists()
    return JsonResponse({"exists": exists})

