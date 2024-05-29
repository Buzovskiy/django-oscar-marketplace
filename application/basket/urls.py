from django.urls import path
from .views import BasketAPIView


urlpatterns = [
    path('', BasketAPIView.as_view()),
]
