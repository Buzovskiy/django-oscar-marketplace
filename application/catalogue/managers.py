from django.db.models import Prefetch

from oscar.apps.catalogue.managers import \
    AttributeFilter as AttributeFilterCore, \
    ProductQuerySet as ProductQuerySetCore, \
    CategoryQuerySet as CategoryQuerySetCore

from oscar.core.loading import get_model


class AttributeFilter(AttributeFilterCore):
    pass


class ProductQuerySet(ProductQuerySetCore):

    def prefetch_child_products_attributes(self):
        ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
        queryset_attributes = ProductAttributeValue.objects.select_related('attribute').all()
        return self.prefetch_related(
                    Prefetch('children'),
                    Prefetch('children__attributes', queryset=queryset_attributes)
                )

    def prefetch_recommended_products_attributes(self):
        ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
        Product = get_model('catalogue', 'Product')
        queryset_attributes = ProductAttributeValue.objects.select_related('attribute').all()
        return self.prefetch_related(
                    Prefetch('recommended_products', queryset=Product.objects.browsable().all()),
                    Prefetch('recommended_products__attributes', queryset=queryset_attributes)
                )

    def prefetch_product_attributes(self):
        ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
        queryset_attributes = ProductAttributeValue.objects.select_related('attribute').all()
        return self.prefetch_related(
                    Prefetch('attributes', queryset=queryset_attributes)
                )


class CategoryQuerySet(CategoryQuerySetCore):
    pass
