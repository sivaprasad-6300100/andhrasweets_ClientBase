from django.shortcuts import render

# Create your views here.


def login_view(request):
    return render(request,'login.html')

def register_view(request):
    return render(request,'register.html')

def profile_view(request):
    return render(request,'profile.html')

def account_view(request):
    return render(request,'account.html')