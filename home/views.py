from django.shortcuts import render
from products.models import Product

def index(request):
    """A view to return the index page with random products"""
    
    # Fetch all products
    all_products = Product.objects.all()

    # Randomize and select 4 products
    randomised = all_products.order_by("?")[:4]

    # Render the template with randomized products
    return render(request, 'home/index.html', {'randomised': randomised})

