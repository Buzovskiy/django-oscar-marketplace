import oscar.apps.catalogue.apps as apps
from oscar.core.loading import get_class
from django.urls import path


class CatalogueConfig(apps.CatalogueConfig):
    name = 'application.catalogue'
    api_products_view = None

    def ready(self):
        super(CatalogueConfig, self).ready()
        from .views import get_products_list
        self.api_products_view = get_products_list

    def get_urls(self):
        urls = super(CatalogueConfig, self).get_urls()
        urls += [
            path('v1/products/list', self.api_products_view, name='api-products-list')
        ]
        return self.post_process_urls(urls)
