from django.urls import path
from .views import BasketAPIView, BasketDeleteAPIView


urlpatterns = [
    path('', BasketAPIView.as_view()),
    path('<int:pk>/', BasketDeleteAPIView.as_view()),
]
