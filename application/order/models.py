from django.db import models
from django.utils.translation import gettext_lazy as _
from oscar.apps.address.abstract_models import AbstractShippingAddress
from oscar.apps.order.abstract_models import AbstractOrder
from application.payment.models import PaymentMethod


class ShippingAddress(AbstractShippingAddress):
    email = models.EmailField(blank=False, null=True)
    base_fields = hash_fields = ['salutation', 'line1', 'line2', 'line3', 'line4', 'state', 'postcode']

    def get_data_for_notification(self):
        data = {}
        data[_('First name')] = self.first_name if self.first_name else ''
        data[_('Last name')] = self.last_name if self.last_name else ''
        data[_('Email')] = self.email if self.email else ''
        data[_('Phone number')] = self.phone_number if self.phone_number else ''
        data[_("Street")] = self.line1 if self.line1 else ''  #
        data[_("Street number")] = self.line2 if self.line2 else ''  #
        data[_('Appartment number')] = self.line4 if self.line4 else ''  #
        data[_('City')] = self.line3 if self.line3 else ''
        data[_('Postal code')] = self.postcode if self.postcode else ''
        data[_('Additional')] = self.notes if self.notes else ''  #
        return data


class Order(AbstractOrder):

    payment_method = models.ForeignKey(
        PaymentMethod, verbose_name=_('Payment method'),
        null=True, on_delete=models.SET_NULL)

    @property
    def data_for_voucher_notification(self):
        voucher = self.discounts.first()
        if not voucher:
            return None
        return _('Promo code'), voucher.voucher_code


from oscar.apps.order.models import *  # noqa isort:skip
