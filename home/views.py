from django.shortcuts import render
from products.models import Product

def index(request):
    """A view to return the index page with top-rated products"""

    # Fetch top-rated products ordered by rating (highest first)
    top_rated_products = Product.objects.order_by('-rating')[:4]

    # Render the template with top-rated products
    return render(request, 'home/index.html', {'randomised': top_rated_products})
