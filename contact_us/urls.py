from django.urls import path
from .views import contact_us , contact_success

urlpatterns = [
    path('contact/', contact_us, name='contact_us'),
    path('contact_us/success/', contact_success, name='contact_success'),
]