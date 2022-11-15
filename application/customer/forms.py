from django import forms
from django.utils.translation import gettext_lazy as _
from oscar.apps.customer.forms import EmailAuthenticationForm as CoreEmailAuthenticationForm, \
    EmailUserCreationForm as CoreEmailUserCreationForm


class EmailAuthenticationForm(CoreEmailAuthenticationForm):
    username = forms.EmailField(
        label=_('Email address'),
        widget=forms.EmailInput(attrs={
            'placeholder': _('Email')
        })
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': _('Password'),
        }),
    )


class EmailUserCreationForm(CoreEmailUserCreationForm):
    email = forms.EmailField(
        label=_('Email address'),
        widget=forms.EmailInput(attrs={
            'placeholder': _('Email')
        })
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Password'),
            }
        )
    )
    password2 = forms.CharField(
        label=_('Confirm password'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Repeat password'),
            }
        )
    )
