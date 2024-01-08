from django.urls import path
import oscar.apps.partner.apps as apps
from oscar.core.loading import get_class
from django.http import HttpResponse


class PartnerConfig(apps.PartnerConfig):
    name = 'application.partner'
    stores_list_view = None
    namespace = 'partner'
