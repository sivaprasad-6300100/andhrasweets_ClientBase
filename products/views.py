from django.shortcuts import render ,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Products
from django.db.models import Avg
from .models import Banner
from reviews.models import Review_Model
# from .models import Blog_

# Create your views here.

def home(request):
    veg_pickles = Products.objects.filter(category="veg-pickles")
    nonveg_pickles = Products.objects.filter(category="nonveg-pickles")
    sweets = Products.objects.filter(category="sweets")
    podis = Products.objects.filter(category="podis")
    savories = Products.objects.filter(category="savories")
    dry_fruits = Products.objects.filter(category="dry-fruits")
    reviews = Review_Model.objects.all().order_by('-created_at')[:6]

    return render(request, "home.html", {
        "veg_pickles": veg_pickles,
        "nonveg_pickles": nonveg_pickles,
        "sweets": sweets,
        "podis": podis,
        "savories": savories,
        "dry_fruits": dry_fruits,
        "reviews": reviews,
    })

# ==============single pages=================
def privacy(request):
    return render(request,'privacy.html')
def terms_conditions(request):
    return render(request,'terms_conditions.html')
def delivery_policy(request):
    return render(request,'delivery_policy.html')
def refund_return(request):
    return render(request,'refund_return.html')




def about(request):
    return render(request, 'about.html')

# def blog(request):
    # return render(request,'blog.html')

def contact(request):
    return render(request, 'contact.html')




# --------------------
# Category Pages
# --------------------

def sweets(request):
    banner = Banner.objects.filter(page="sweets").first()

    sweets = Products.objects.filter(category="sweets")

    return render(request, "sweets.html",{
        "baneer":banner,
        "sweets":sweets,

    })

# pickles page view


def pickles(request):
    banner = Banner.objects.filter(page="pickles").first()

    veg_pickles = Products.objects.filter(category="veg-pickles")
    nonveg_pickles = Products.objects.filter(category="nonveg-pickles")

    return render(request, "pickles.html", {
        "banner": banner,
        "veg_pickles": veg_pickles,
        "nonveg_pickles": nonveg_pickles,
    })


# dry fruits page view 

def dry_fruits(request):
    banner =Banner.objects.filter(page="dry-fruits").first()
    return render(request, "dry_fruits.html",{"banner": banner})

# savories page view

def savories(request):
    banner = Banner.objects.filter(page="savories").first()

    savories = Products.objects.filter(category="savories")

    return render(request, "savories.html", {
        "banner": banner,
        "savories": savories,
    })


# masalas and podi page view 

def podis(request):
    banner = Banner.objects.filter(page="podis").first()

    podis =Products.objects.filter(category="podis")

    return render(request, "podis.html",{
        "banner": banner,
        "podis": podis,
    })

# --------------------
# Product Details
# --------------------


def can_review(user):
    return user.is_authenticated and user.is_verified


# @login_required
def product_detail(request, id):
    product = get_object_or_404(Products, id=id)

    # ⭐ Average rating for this product
    avg_rating = product.reviews.aggregate(
        Avg("rating")
    )["rating__avg"] or 0

    # 📝 All reviews of this product
    reviews = product.reviews.all().order_by("-created_at")

    # 🔐 Can this user review?
    can_user_review = can_review(request.user)

    # 📝 Handle review submit
    if request.method == "POST" and can_user_review:
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if rating and comment:
            Review_Model.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    "name": request.user.name,
                    "rating": rating,
                    "comment": comment
                }
            )
        return redirect("product_detail", id=id)

    return render(request, "product_detail.html", {
        "product": product,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "can_user_review": can_user_review,
    })


