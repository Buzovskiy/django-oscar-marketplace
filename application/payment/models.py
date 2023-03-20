from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentMethod(models.Model):
    title = models.CharField(
        _('Title'),
        help_text=_('Payment method that will be shown on the checkout page'),
        max_length=255,
        blank=False,
        null=False
    )
    objects = models.Manager()

    def __str__(self):
        return self.title


from oscar.apps.payment.models import *  # noqa isort:skip
