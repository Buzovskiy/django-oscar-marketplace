import re
from extra_views import ModelFormSetView
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect, render
from oscar.core.loading import get_class, get_model, get_classes
from oscar.apps.checkout.views import PaymentDetailsView as PaymentDetailsViewCore
from oscar.apps.checkout.session import CheckoutSessionMixin
from .forms import PaymentMethodForm, ShippingAddressForm, ShippingMethodForm
from application.shipping.repository import Repository


(BasketLineForm, AddToBasketForm, BasketVoucherForm, SavedLineForm) = get_classes(
    'basket.forms', ('BasketLineForm', 'AddToBasketForm',
                     'BasketVoucherForm', 'SavedLineForm'))
BasketLineFormSet = get_class('basket.formsets', 'BasketLineFormSet')
Country = get_model('address', 'country')


class CheckoutViewMixin:
    checkout_session = None
    _shipping_methods = None
    request = None

    def get_shipping_address_form_initial(self):
        initial = self.checkout_session.new_shipping_address_fields()
        if initial:
            initial = initial.copy()
            # Convert the primary key stored in the session into a Country
            # instance
            try:
                initial['country'] = Country.objects.get(
                    iso_3166_1_a2=initial.pop('country_id'))
            except Country.DoesNotExist:
                # Hmm, the previously selected Country no longer exists. We
                # ignore this.
                pass
        return initial

    def get_payment_method_form_initial(self):
        return self.checkout_session.get_payment_method_fields()

    def get_shipping_method_form_initial(self):
        return self.checkout_session.get_shipping_method_fields()

    def get_available_shipping_methods(self):
        """
        Returns all applicable shipping method objects for a given basket.
        """
        # Shipping methods can depend on the user, the contents of the basket
        # and the shipping address (so we pass all these things to the
        # repository).  I haven't come across a scenario that doesn't fit this
        # system.
        return Repository().get_shipping_methods(
            basket=self.request.basket, user=self.request.user,
            shipping_addr=self.get_shipping_address(self.request.basket),
            request=self.request)


class OnePageCheckoutView(CheckoutViewMixin, CheckoutSessionMixin, TemplateView):
    template_name = 'oscar/checkout/one_page_checkout.html'
    success_url = reverse_lazy('checkout:preview')
    _shipping_methods = None

    pre_conditions = [
        'check_basket_is_not_empty',
        'check_basket_is_valid']

    def get(self, request, *args, **kwargs):
        self._shipping_methods = self.get_available_shipping_methods()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shipping_address_form'] = ShippingAddressForm(
            initial=self.get_shipping_address_form_initial())
        context['payment_method_form'] = PaymentMethodForm(
            prefix='payment-method', initial=self.get_payment_method_form_initial())
        context['shipping_method_form'] = ShippingMethodForm(
            prefix='shipping-method',
            methods=self._shipping_methods,
            initial=self.get_shipping_method_form_initial()
        )
        context['form_is_valid'] = True
        return context

    def post(self, request, *args, **kwargs):
        self._shipping_methods = self.get_available_shipping_methods()
        context = self.get_context_data(**kwargs)

        shipping_address_form = ShippingAddressForm(request.POST)
        payment_method_form = PaymentMethodForm(request.POST, prefix='payment-method')
        shipping_method_form = ShippingMethodForm(
            request.POST, methods=self._shipping_methods, prefix='shipping-method')

        if shipping_address_form.is_valid() and payment_method_form.is_valid() and shipping_method_form.is_valid():
            # <process form cleaned data>
            self.valid_shipping_address_form(shipping_address_form)
            self.valid_payment_method_form(payment_method_form)
            self.checkout_session.use_shipping_method(
                shipping_method_form.cleaned_data['method_code'])
            return HttpResponseRedirect(self.success_url)
        else:
            context['form_is_valid'] = False

        context['shipping_address_form'] = shipping_address_form
        context['payment_method_form'] = payment_method_form
        context['shipping_method_form'] = shipping_method_form

        return render(request, self.template_name, context=context)

    def valid_shipping_address_form(self, form):
        # Store the address details in the session
        address_fields = dict(
            (k, v) for (k, v) in form.instance.__dict__.items()
            if not k.startswith('_'))
        self.checkout_session.ship_to_new_address(address_fields)

    def valid_payment_method_form(self, form):
        # Store the payment method details in the session.
        # Remove prefix from input name.
        fields = dict(
            (re.sub('^payment-method-', '', k), v) for (k, v) in form.data.items()
            if k.startswith('payment-method-'))
        self.checkout_session.set_payment_method_fields(fields)


class PaymentDetailsView(CheckoutViewMixin, PaymentDetailsViewCore):

    def get(self, request, *args, **kwargs):
        self._shipping_methods = self.get_available_shipping_methods()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shipping_address'] = self.get_shipping_address_form_initial()
        context['payment_method_object'] = self.checkout_session.get_payment_method_object()
        context['shipping_method_object'] = self.checkout_session.get_shipping_method_object()
        return context
