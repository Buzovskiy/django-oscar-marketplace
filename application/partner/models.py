from django.db import models
from django.utils.translation import gettext_lazy as _
from oscar.apps.partner.abstract_models import AbstractStockRecord


class StockRecord(AbstractStockRecord):
    # discount in percents, e.g: 10.
    discount_1c = models.DecimalField(
        _("Value"), decimal_places=2, max_digits=12, null=True, blank=True)
    price_initial_1c = models.DecimalField(
        _("Price"), decimal_places=2, max_digits=12,
        blank=True, null=True)


class Retail(models.Model):
    title = models.CharField(
        _('Title'),
        max_length=255,
        unique=True,
        blank=False,
        help_text=_('Enter the title of retail partner stores')
    )

    class Meta:
        verbose_name = _('Retail shop partner')
        verbose_name_plural = _('Retail shop partners')

    def __str__(self):
        return self.title


class RetailCity(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    country = models.ForeignKey('address.Country', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Retail city')
        verbose_name_plural = _('Retail cities')


class RetailAddress(models.Model):
    retail = models.ForeignKey(Retail, on_delete=models.CASCADE)
    retail_city = models.ForeignKey('partner.RetailCity', on_delete=models.CASCADE, null=True)
    short_description = models.CharField(
        _('Short description'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Enter short description which will be displayed in parenthesis near title or leave field empty')
    )
    address = models.CharField(
        _('Address'),
        max_length=255,
        help_text=_('Enter address of the retail partner store'),
    )
    shop_working_hours = models.CharField(
        _('Store working hours'),
        max_length=255,
        blank=True,
        help_text=_('Enter store working hours')
    )
    website = models.CharField(_('Web site'), max_length=255, blank=True, help_text=_('Enter web site'))
    latitude = models.FloatField(
        _('Latitude'),
        blank=True,
        null=True,
        help_text=_('Enter latitude coordinate in decimal format, for example 46.43143143569561')
    )
    longitude = models.FloatField(
        _('longitude'),
        blank=True,
        null=True,
        help_text=_('Enter longitude coordinate in decimal format, for example 30.724300888157735')
    )

    def __str__(self):
        # return f"{self.country.printable_name} ({self.address})"
        return self.address

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')


from oscar.apps.partner.models import *  # noqa isort:skip
