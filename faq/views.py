from django.shortcuts import render

# Create your views here.

#Renders the FAQ page
def faq_page(request):

    return render(request, "faq/faq.html")