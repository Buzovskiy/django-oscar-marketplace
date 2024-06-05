from django.urls import path
from .webhook_views import stripe_webhook_view


urlpatterns = [
    path('stripe-webhook/', stripe_webhook_view),
]
