from django.core.exceptions import ObjectDoesNotExist
from oscar.apps.checkout.session import CheckoutSessionMixin as CheckoutSessionMixinCore
from application.payment.models import PaymentMethod


class CheckoutSessionMixin(CheckoutSessionMixinCore):

    def get_payment_method(self):
        """
        We instantiate ``PaymentMethod`` model with the appropriate form data (which
        is saved in the session)
        :return: instance of ``PaymentMethod`` model
        """
        payment_method_data = self.checkout_session.get_payment_method_fields()
        if payment_method_data:
            try:
                obj_id = payment_method_data['title']
                payment_method = PaymentMethod.objects.get(pk=obj_id)
            except ObjectDoesNotExist:
                return None
            return payment_method

    def build_submission(self, **kwargs):
        submission = super().build_submission(**kwargs)
        payment_method = self.get_payment_method()
        submission['order_kwargs'].update({'payment_method': payment_method})

        return submission
