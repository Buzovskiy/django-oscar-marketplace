from django.db import models
from django.utils.translation import gettext_lazy as _


class SearchOptimisationFields(models.Model):
    page_name = models.CharField(_('Meta page name'), max_length=254, unique=True)
    meta_title = models.TextField(_('Meta title'), null=True, blank=True)
    meta_description = models.TextField(_('Meta description'), null=True, blank=True)
    meta_keywords = models.TextField(_('Meta keywords'), null=True, blank=True)
    page_url = models.CharField(_('Url of the page'), max_length=254, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.page_name

    class Meta:
        verbose_name = _('Search optimisation fields')
        verbose_name_plural = _('Search optimisation fields')
