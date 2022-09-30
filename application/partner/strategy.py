from django.db.models import F
from oscar.apps.partner.strategy import StockRequired, NoTax, Structured


class Selector(object):
    """
    Responsible for returning the appropriate strategy class for a given
    user/session.

    This can be called in three ways:

    #) Passing a request and user. This is for determining
       prices/availability for a normal user browsing the site.

    #) Passing just the user. This is for offline processes that don't
       have a request instance but do know which user to determine prices for.

    #) Passing nothing. This is for offline processes that don't
       correspond to a specific user, e.g., determining a price to store in
       a search index.

    """

    def strategy(self, request=None, user=None, **kwargs):
        """
        Return an instantiated strategy instance
        """
        # Default to the backwards-compatible strategy of picking the first
        # stockrecord but charging zero tax.
        return Default(request)


class UseFirstStockRecord(object):
    """
    Stockrecord selection mixin for use with the ``Structured`` base strategy.
    This mixin picks the first (normally only) stockrecord to fulfil a product.
    """

    def select_stockrecord(self, product):
        # return product.stockrecords.filter(num_in_stock__gt=0).filter(num_in_stock__gt=F('num_allocated')).first()
        return product.stockrecords.first()


class Default(UseFirstStockRecord, StockRequired, NoTax, Structured):
    """
    Default stock/price strategy that uses the first found stockrecord for a
    product, ensures that stock is available (unless the product class
    indicates that we don't need to track stock) and charges zero tax.
    """

