import re
import json
import stripe
from extra_views import ModelFormSetView
from django import http
from django.views.generic import TemplateView, FormView
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect, render
from django.utils.translation import get_language
from oscar.core.loading import get_class, get_model, get_classes
from oscar.apps.checkout.views import PaymentDetailsView as PaymentDetailsViewCore
from oscar.apps.checkout.session import CheckoutSessionMixin
from .forms import PaymentMethodForm, ShippingAddressForm, ShippingMethodForm
from application.shipping.repository import Repository
from application.basket.models import Basket
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from app_settings.models import AppSettings
from .serializers import PaymentIntentSerializer

(BasketLineForm, AddToBasketForm, BasketVoucherForm, SavedLineForm) = get_classes(
    'basket.forms', ('BasketLineForm', 'AddToBasketForm',
                     'BasketVoucherForm', 'SavedLineForm'))
BasketLineFormSet = get_class('basket.formsets', 'BasketLineFormSet')
Country = get_model('address', 'country')


@csrf_exempt
@api_view(['POST'])
def stripe_webhook_view(request):
    # payload = request.body
    # event = None
    #
    # try:
    #     event = stripe.Event.construct_from(
    #         json.loads(payload), stripe.api_key
    #     )
    # except ValueError as e:
    #     # Invalid payload
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    # # Handle the event
    # if event.type == 'payment_intent.succeeded':
    #     payment_intent = event.data.object  # contains a stripe.PaymentIntent
    #     # Then define and call a method to handle the successful payment intent.
    #     # handle_payment_intent_succeeded(payment_intent)

    return Response(status=status.HTTP_200_OK)
