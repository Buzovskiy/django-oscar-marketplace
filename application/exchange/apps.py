from oscar.core.application import OscarConfig
from django.urls import path
from oscar.core.loading import get_class
from django.views.decorators.csrf import csrf_exempt


class ExchangeConfig(OscarConfig):
    index_view = None
    name = 'application.exchange'
    namespace = 'exchange'

    def ready(self):
        self.index_view = get_class('exchange.views', 'IndexView')

    def get_urls(self):
        urls = [
            path('', csrf_exempt(self.index_view.as_view()), name='index'),
        ]
        return self.post_process_urls(urls)
