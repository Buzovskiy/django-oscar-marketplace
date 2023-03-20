from django.core.exceptions import ObjectDoesNotExist
from oscar.apps.checkout.utils import CheckoutSessionData as CheckoutSessionDataCore
from application.payment.models import PaymentMethod
from application.shipping.repository import Repository


class CheckoutSessionData(CheckoutSessionDataCore):

    def set_payment_method_fields(self, payment_method_fields):
        """
        Use a manually entered payment method
        """
        self._unset('payment_method', 'new_payment_method')
        self._set('payment_method', 'new_payment_method', payment_method_fields)

    def get_payment_method_fields(self):
        """
        Return payment method fields
        """
        return self._get('payment_method', 'new_payment_method')

    def get_shipping_method_fields(self):
        """
        Return shipping method fields
        """
        method_code = self._get('shipping', 'method_code')
        if method_code is not None:
            return {'method_code': method_code}
        return None

    def get_payment_method_object(self):
        """
        Method that returns  payment method object by payment method
        information provided in session
        :return: model object or None
        """
        payment_method_id = self.get_payment_method_fields()['title']
        try:
            payment_method_id = int(payment_method_id)
            payment_method_object = PaymentMethod.objects.get(pk=payment_method_id)
        except (ValueError, ObjectDoesNotExist) as e:
            payment_method_object = None
        return payment_method_object

    def get_shipping_method_object(self):
        """
        Method that returns shipping method object by shipping method
        information provided in session
        :return: object or None
        """
        method_code = None
        if 'method_code' in self.get_shipping_method_fields() \
                and len(Repository.methods) > 0:
            method_code = self.get_shipping_method_fields()['method_code']
            def filter_by_code(method_object): return method_object.code == method_code
            shipping_method_objects_list = list(filter(filter_by_code, Repository.methods))
            try:
                return shipping_method_objects_list[0]
            except IndexError:
                pass
        return None
