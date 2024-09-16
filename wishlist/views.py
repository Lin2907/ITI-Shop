from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist
from products.models import Product

# Create your views here.


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if product in wishlist.products.all():
        messages.info(request, "This product is already in your wishlist.")
    else:
        wishlist.products.add(product)
        messages.success(request, "Product added to your wishlist.")

    return redirect("product_detail", product_id=product_id)


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, "Product removed from your wishlist.")
    else:
        messages.info(request, "This product is not in your wishlist.")

    return redirect("wishlist_view")


@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()

    return render(
        request, "wishlist/wishlist.html",
        {"wishlist": wishlist, "products": products}
    )
