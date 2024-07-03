from oscar.apps.catalogue.product_attributes import ProductAttributesContainer as ProductAttributesContainerCore
from oscar_routing.utils import getattr_lang
from django.conf import settings


class ProductAttributesContainer(ProductAttributesContainerCore):
    pass


class PrefetchedProductAttributesContainer:

    def __init__(self, product):
        for v in product.attributes.all():
            setattr(self, v.attribute.code, {
                'value': getattr_lang(v, 'value_text'), 'pav_id': v.id, 'attribute': v.attribute
            })
