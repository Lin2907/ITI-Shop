from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist
from products.models import Product
from profiles.models import UserProfile

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
    if not request.user.is_authenticated:
        messages.error(
            request, "Please log in to add to your Wishlist."
        )
        return redirect(reverse("account_login"))

    user = get_object_or_404(UserProfile, user=request.user)
    wishlist, created = Wishlist.objects.get_or_create(user=user.user)

    template_name = "wishlist/wishlist.html"
    context = {"wishlist": wishlist}
    return render(request, template_name, context)