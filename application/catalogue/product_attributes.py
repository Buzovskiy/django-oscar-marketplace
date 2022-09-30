from oscar.apps.catalogue.product_attributes import ProductAttributesContainer as ProductAttributesContainerCore


class ProductAttributesContainer(ProductAttributesContainerCore):
    pass


class PrefetchedProductAttributesContainer:

    def __init__(self, product):
        for v in product.attributes.all():
            setattr(self, v.attribute.code, {'value': v.value})
