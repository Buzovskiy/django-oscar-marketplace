import oscar.apps.catalogue.apps as apps
from oscar.core.loading import get_class
from django.urls import path, re_path


class CatalogueConfig(apps.CatalogueConfig):
    name = 'application.catalogue'
    api_products_view = product_details_api_view = None

    def ready(self):
        super(CatalogueConfig, self).ready()
        from .views import get_products_list, ProductDetailsAPIView
        self.api_products_view = get_products_list
        self.product_details_api_view = ProductDetailsAPIView

    def get_urls(self):
        urls = super(CatalogueConfig, self).get_urls()
        urls += [
            re_path(
                r'^(?P<product_slug>[\w-]*)_(?P<pk>\d+)/$',
                self.detail_view.as_view(), name='detail'),
            path('v1/products/list', self.api_products_view, name='api-products-list'),
            path('v1/products/<int:pk>', self.product_details_api_view.as_view())
        ]
        return self.post_process_urls(urls)
