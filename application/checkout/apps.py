import oscar.apps.checkout.apps as apps
from django.urls import path
from django.http import HttpResponse
from oscar.core.loading import get_class


class CheckoutConfig(apps.CheckoutConfig):
    name = 'application.checkout'

    def ready(self):
        super(CheckoutConfig, self).ready()
        self.index_view = get_class('checkout.views', 'OnePageCheckoutView')

    def get_urls(self):
        urls = super(CheckoutConfig, self).get_urls()
        urls += [
            path('', self.index_view.as_view(), name='index')
        ]
        return self.post_process_urls(urls)
