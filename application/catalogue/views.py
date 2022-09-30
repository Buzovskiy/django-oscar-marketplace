from django.db.models import Prefetch
from oscar.apps.catalogue.views import ProductDetailView as CoreProductDetailView
from oscar.core.loading import get_model

ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
Product = get_model('catalogue', 'Product')


class ProductDetailView(CoreProductDetailView):

    def get_queryset(self):
        qs = super(ProductDetailView, self).get_queryset()
        queryset_attributes = ProductAttributeValue.objects.select_related('attribute').all()
        qs = qs.prefetch_related(
            Prefetch('attributes', queryset=queryset_attributes),
            Prefetch('recommended_products', queryset=Product.objects.browsable().all()),
            Prefetch('recommended_products__attributes', queryset=queryset_attributes),
            Prefetch('children'),
            Prefetch('children__attributes', queryset=queryset_attributes),
            Prefetch('recommended_products__children'),
            Prefetch('recommended_products__children__attributes', queryset=queryset_attributes),
            Prefetch('recommended_products__recommended_products', queryset=Product.objects.browsable().all()),
            Prefetch('recommended_products__recommended_products__attributes', queryset=queryset_attributes),
        )
        return qs
