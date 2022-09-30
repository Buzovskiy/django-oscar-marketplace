from oscar.core.application import OscarConfig
from django.urls import path
from oscar.core.loading import get_class


class HomeConfig(OscarConfig):
    index_view = None
    name = 'application.home'
    # namespace = 'home'

    def ready(self):
        self.index_view = get_class('home.views', 'IndexView')

    def get_urls(self):
        urls = [
            path('', self.index_view.as_view(), name='home'),
        ]
        return self.post_process_urls(urls)
