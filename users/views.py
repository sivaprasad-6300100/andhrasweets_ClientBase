from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Address

@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, "address_list.html", {"addresses": addresses})

@login_required
def add_address(request):
    if request.method == "POST":
        Address.objects.create(
            user=request.user,
            name=request.POST['name'],
            mobile=request.POST['mobile'],
            address=request.POST['address'],
            landmark=request.POST['landmark'],
        )
        return redirect('address_list')
    return render(request, "add_address.html")

@login_required
def edit_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)

    if request.method == "POST":
        address.name = request.POST['name']
        address.mobile = request.POST['mobile']
        address.address = request.POST['address']
        address.landmark = request.POST['landmark']
        address.save()
        return redirect('address_list')

    return render(request, "edit_address.html", {"address": address})

@login_required
def delete_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)
    address.delete()
    return redirect('address_list')
