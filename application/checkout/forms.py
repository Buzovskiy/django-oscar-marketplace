from django import forms
from django.utils.translation import gettext_lazy as _
from oscar.apps.checkout.forms import ShippingAddressForm as ShippingAddressFormCore, \
    ShippingMethodForm as ShippingMethodFormCore
from application.payment.models import PaymentMethod


class ShippingAddressForm(ShippingAddressFormCore):

    instance = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'phone_number' in self.fields:
            self.fields['phone_number'].widget.attrs.update({
                'placeholder': _('E.g.: +48123456789')
            })

    class Meta(ShippingAddressFormCore.Meta):
        fields = [
            'first_name', 'last_name',
            'phone_number', 'country', 'notes', 'line1', 'email'
        ]


class PaymentMethodForm(forms.Form):
    title = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(),
        empty_label=_('Choose payment method'),
        required=True
    )


class ShippingMethodForm(ShippingMethodFormCore):
    method_code = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        methods = kwargs.pop('methods', [])
        super().__init__(*args, **kwargs)
        self.fields['method_code'].choices = ((m.code, m) for m in methods)
