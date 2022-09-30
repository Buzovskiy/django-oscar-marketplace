from oscar.apps.catalogue.search_handlers import *
from oscar.apps.catalogue.search_handlers import SimpleProductSearchHandler as SimpleProductSearchHandlerCore


class SimpleProductSearchHandler(SimpleProductSearchHandlerCore):
    """
    A basic implementation of the full-featured SearchHandler that has no
    faceting support, but doesn't require a Haystack backend. It only
    supports category browsing.

    Note that is meant as a replacement search handler and not as a view
    mixin; the mixin just does most of what we need it to do.
    """
    def get_queryset(self):
        qs = Product.objects.browsable().base_queryset().prefetch_child_products_attributes()
        qs = qs.prefetch_recommended_products_attributes()
        qs = qs.prefetch_product_attributes()
        if self.categories:
            qs = qs.filter(categories__in=self.categories).distinct()
        return qs
