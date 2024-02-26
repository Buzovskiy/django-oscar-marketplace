import logging
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

            Prefetch('parent'),
            Prefetch('parent__attributes', queryset=queryset_attributes),
            Prefetch('parent__recommended_products'),
            Prefetch('parent__recommended_products__attributes', queryset=queryset_attributes),
            Prefetch('parent__recommended_products__recommended_products', queryset=Product.objects.browsable().all()),
            Prefetch('parent__recommended_products__recommended_products__attributes', queryset=queryset_attributes),
        )

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        logging.basicConfig(format='%(asctime)s - %(message)s')
        logger = logging.getLogger('product_detail_ctx')
        for product in ctx['product'].recommended_products.all():
            logger.warning(f"{product.upc} - is public={product.is_public}")
        return ctx
