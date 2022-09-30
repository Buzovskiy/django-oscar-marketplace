from django.urls import path
import oscar.apps.partner.apps as apps
from oscar.core.loading import get_class
from django.http import HttpResponse


class PartnerConfig(apps.PartnerConfig):
    name = 'application.partner'
    stores_list_view = None
    namespace = 'partner'

    def ready(self):
        self.stores_list_view = get_class('partner.views', 'StoresListView')

    def get_urls(self):
        urls = [
            path('stores/', self.stores_list_view.as_view(), name='stores'),
        ]
        return self.post_process_urls(urls)
