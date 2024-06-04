from django.urls import path
from .views import PaymentIntentApiView


urlpatterns = [
    path('payment-intent/', PaymentIntentApiView.as_view()),
]
