from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .forms import ContactForm
from .models import Contact


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            confirm_query(contact)
            messages.success(request,
                             "Your inquiry has been sent successfully!")
            return redirect(reverse("contact_success"))
        else:
            messages.error(request, "Please check if the form is valid.")
    else:
        form = ContactForm()

    template = "contact_us/contact_us.html"
    context = {
        "form": form,
    }

    return render(request, template, context)


def confirm_query(contact_us):

    cust_email = contact_us.email
    subject = render_to_string(
        "contact_us/email_templates/contact_subject.txt",
        {"contact_us": contact_us},
    )
    body = render_to_string(
        "contact_us/email_templates/contact_body.txt",
        {"contact_us": contact_us,
         "contact_email": settings.DEFAULT_FROM_EMAIL},
    )

    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [cust_email])


def contact_success(request):

    return render(request, "contact_us/contact_success.html")