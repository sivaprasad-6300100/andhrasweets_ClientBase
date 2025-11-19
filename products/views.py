from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')

def contact(request):
    return render(request, 'contact.html')


# --------------------
# Category Pages
# --------------------

def sweets(request):
    return render(request, 'sweets.html')

def pickles(request):
    return render(request, 'pickles.html')

def dry_fruits(request):
    return render(request, 'dry_fruits.html')

def savories(request):
    return render(request, 'savories.html')

def masalas_podis(request):
    return render(request, 'masalas.html')


# --------------------
# Product Details
# --------------------

def product_detail(request, id):
    return render(request, 'product_detail.html', {'id': id})

 