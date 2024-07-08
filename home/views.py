from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from .forms import NewsletterSignupForm

def index(request):
    """A view to return the index page with random products"""
    
    # Fetch all products
    all_products = Product.objects.all()

    # Randomize and select 4 products
    randomised = all_products.order_by("?")[:4]

    # Render the template with randomized products
    return render(request, 'home/index.html', {'randomised': randomised})

def newsletter_signup(request):
    """A view to handle newsletter signups"""
    if request.method == 'POST':
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully signed up for the newsletter.')
            return render(request, 'home/newsletter_signup.html', {'form': form})
        else:
            messages.error(request, 'There was an error with your signup.')
            return render(request, 'home/index.html')
    else:
        form = NewsletterSignupForm()
    
    