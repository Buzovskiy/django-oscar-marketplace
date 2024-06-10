import re
import json
import stripe
from django.http import HttpResponse
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
from application.shipping.methods import NoShippingRequired, FixedPrice
from application.basket.models import Basket
from application.order.models import ShippingAddress, Order
from application.order.utils import OrderCreator
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
    """
    When payment intent is confirmed, Stripe webhook is triggered and this view is called.
    The body of the POST request contains data having content-type application/json.
    This data has dictionary metadata with information about user basket and future order checkout data
    which was passed on payment intent create.
    """
    try:
        metadata = request.data['data']['object']['metadata']
    except KeyError as e:
        return HttpResponse(e, status=400)

    basket_id = metadata.get('basketId', None)
    try:
        basket = Basket.objects.get(id=basket_id)
    except Basket.DoesNotExist as e:
        return HttpResponse(e, status=200)

    if basket.is_submitted:
        return HttpResponse(f'Basket with id {basket.id} is already submitted', status=200)

    order_number = metadata.get('orderNumber')
    if Order.objects.filter(number=order_number).count():
        return HttpResponse(f'Order with id {order_number} already exists', status=200)

    shippingDetails = json.loads(metadata['shippingDetails'])

    try:
        carrier = json.loads(metadata['carrier'])
    except KeyError:
        carrier = None

    shipping_address_data = {}
    # todo: make serializer for shipping address instead of data verifications below
    if 'email' in shippingDetails:
        shipping_address_data['email'] = shippingDetails['email']
    if 'phoneNumber' in shippingDetails:
        shipping_address_data['phone_number'] = shippingDetails['phoneNumber']
    if 'additional' in shippingDetails:
        shipping_address_data['notes'] = shippingDetails['additional']
    if 'firstName' in shippingDetails:
        shipping_address_data['first_name'] = shippingDetails['firstName']
    if 'lastName' in shippingDetails:
        shipping_address_data['last_name'] = shippingDetails['lastName']
    if 'street' in shippingDetails:
        shipping_address_data['line1'] = shippingDetails['street']
    if 'streetNumber' in shippingDetails:
        shipping_address_data['line2'] = shippingDetails['streetNumber']
    if 'city' in shippingDetails:
        shipping_address_data['line3'] = shippingDetails['city']
    shipping_address_data['state'] = ''
    if 'postalCode' in shippingDetails:
        shipping_address_data['postcode'] = shippingDetails['postalCode']
    else:
        shipping_address_data['postcode'] = ''
    try:
        country = Country.objects.filter(iso_3166_1_a2='ES').get()
    except Country.DoesNotExist as e:
        return HttpResponse(e, status=200)
    shipping_address_data['country'] = country
    shipping_address_data['search_text'] = ''

    # Save shipping address
    # shipping_address = ShippingAddress.objects.create(**shipping_address_data)
    #
    # # Get shipping method
    # shipping_method = carrier['name'] if carrier is not None else ''
    #
    # order = OrderCreator().place_order(
    #     user=None,
    #     order_number=order_number,
    #     basket=basket,
    #     shipping_address=shipping_address,
    #     shipping_method=shipping_method,
    #     # shipping_charge=shipping_charge,
    #     # total=order_total,
    #     # billing_address=billing_address,
    #     # status=status,
    #     # request=request,
    #     # surcharges=surcharges,
    #     # **kwargs
    # )
    # # self.save_payment_details(order)

    return Response(status=status.HTTP_200_OK)
