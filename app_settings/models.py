from django.db import models
from django.utils.translation import gettext_lazy as _


class StripeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(key='stripe_api_key')


class AppSettings(models.Model):
    title = models.CharField(_('Title'), max_length=255, blank=False, null=False)
    key = models.CharField(_('Key'), max_length=255, blank=False, null=False, unique=True)
    value = models.CharField(_('Value'), max_length=255, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)

    objects = models.Manager()
    stripe_api_key = StripeManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Application settings')
        verbose_name_plural = _('Application settings')
