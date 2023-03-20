from django.db import models
from django.utils.translation import gettext_lazy as _
from oscar.apps.address.abstract_models import AbstractShippingAddress
from oscar.apps.order.abstract_models import AbstractOrder
from application.payment.models import PaymentMethod


class ShippingAddress(AbstractShippingAddress):
    email = models.EmailField(blank=False, null=True)


class Order(AbstractOrder):

    payment_method = models.ForeignKey(
        PaymentMethod, verbose_name=_('Payment method'),
        null=True, on_delete=models.SET_NULL)


from oscar.apps.order.models import *  # noqa isort:skip
