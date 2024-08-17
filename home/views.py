from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from .models import NewsletterSignup
from .forms import NewsletterSignupForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

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
            messages.error(request, 'Registration error. Please verify your email address.')
            return render(request, 'home/index.html')
    else:
        form = NewsletterSignupForm()

#Email confirmation to user

def confirm_newsletter(newsletter_signup):
    
    cust_email = newsletter_signup.email
    subject = render_to_string(
        "home/email_templates/newsletter_subject.txt",
        {"newsletter_signup": newsletter_signup},
    )
    body = render_to_string(
        "home/email_templates/newsletter_body.txt",
        {"newsletter_signup": newsletter_signup, "contact_email": settings.DEFAULT_FROM_EMAIL},
    )

    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [cust_email])
    
    
    # 404 and 500 error views

def custom_404(request, exception):
    return render(request, 'home/404.html', status=404)


def custom_500(request):
    return render(request, 'home/500.html', status=500)
