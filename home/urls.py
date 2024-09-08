# home/urls.py
from django.urls import path
from .views import index, newsletter_signup, privacy_policy

urlpatterns = [
    path("", index, name="index"),
    path("newsletter_signup/", newsletter_signup, name="newsletter_signup"),
    path("privacy_policy/", privacy_policy, name="privacy_policy"),
]
