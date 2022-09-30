from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.mail import mail_managers
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from captcha.fields import CaptchaField


class ContactsForm(forms.Form):
    name = forms.CharField(
        label=_('Name'),
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': f'{_("Name")}*'.lower()}),
    )
    last_name = forms.CharField(
        label=_('Last name'),
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': f'{_("Last name")}'.lower()}),
        required=False,
    )
    email = forms.EmailField(
        label=_('Email'),
        max_length=255,
        widget=forms.EmailInput(attrs={'placeholder': f'{_("email")}*'.lower()})
    )
    phone = forms.CharField(
        label=_('Telephone'),
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': f'{_("Telephone")}*'.lower()}),
        help_text=_('Start with country phone code')
    )
    country = forms.CharField(
        label=_('Country'),
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': f'{_("Country")}*'.lower()}),
    )
    city = forms.CharField(
        label=_('City'),
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': f'{_("City")}*'.lower()}),
    )
    postal_code = forms.CharField(
        label=_('Postal code'),
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': f'{_("Postal code")}'.lower()}),
        required=False,
    )
    subject = forms.CharField(
        label=_('Subject'),
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': f'{_("Subject")}*'.lower()}),
    )
    message = forms.CharField(
        label=_('Your message'),
        max_length=1000,
        widget=forms.Textarea(attrs={'placeholder': f'{_("your message")}*'.lower(), 'rows': 4})
    )
    shop_question = forms.ChoiceField(
        label=_("Do you already have a shop?"),
        choices=(("", _("Do you already have a shop?")), ("no", _("No")), ("yes", _("Yes")))
    )
    shop_sign = forms.CharField(
        label=_('Shop sign'),
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': f'{_("Shop sign")}'.lower()}),
        required=False
    )
    website = forms.CharField(
        label=_('Website'),
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': f'{_("Website")}'.lower()}),
        required=False
    )
    accept = forms.BooleanField(
        label=_('Accept'),
        required=True,
    )
    captcha = CaptchaField(label=_('Captcha'),)

    def send_email(self, request):
        current_site = Site.objects.get_current()
        data = {}
        for field_name, field_obj in self.fields.items():
            if field_name in self.cleaned_data:
                data[field_obj.label] = self.cleaned_data[field_name]
        context = {
            'contacts_uri': request.build_absolute_uri(''),
            'data': data,
        }
        html_message = render_to_string(template_name='contacts/email.html', context=context)
        subject = f'{current_site.domain} | <{self.cleaned_data["email"]}>'
        mail_managers(
            subject=subject,
            message=html_message,
            html_message=html_message,
            fail_silently=False,
        )
