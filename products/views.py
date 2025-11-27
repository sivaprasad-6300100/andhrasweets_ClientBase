from django.shortcuts import render
from .models import Products
from .models import Banner

# Create your views here.

def home(request):
    veg_pickles = Products.objects.filter(category="veg-pickles")
    nonveg_pickles = Products.objects.filter(category="non-veg-pickles")
    sweets = Products.objects.filter(category="sweets")
    podis = Products.objects.filter(category="podis")
    savories = Products.objects.filter(category="savories")
    dry_fruits = Products.objects.filter(category="dry-fruits")

    return render(request, "home.html", {
        "veg_pickles": veg_pickles,
        "nonveg_pickles": nonveg_pickles,
        "sweets": sweets,
        "podis": podis,
        "savories": savories,
        "dry_fruits": dry_fruits,
    })



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
    banner = Banner.objects.filter(page="sweets").first()
    return render(request, "sweets.html", {"banner": banner})

# pickles page view


def pickles(request):
    banner = Banner.objects.filter(page="pickles").first()
    return render(request, "pickles.html", {"banner": banner})


# dry fruits page view 

def dry_fruits(request):
    banner =Banner.objects.filter(page="dry-fruits").first()
    return render(request, "dry_fruits.html",{"banner": banner})

# savories page view

def savories(request):
    banner = Banner.objects.filter(page="savories").first()
    return render(request, "savories.html", {"banner": banner})


# masalas and podi page view 

def masalas_podis(request):
    banner = Banner.objects.filter(page="podis").first()
    return render(request, "podis.html", {"banner": banner})

# --------------------
# Product Details
# --------------------

def product_detail(request, id):
    return render(request, 'product_detail.html', {'id': id})

 