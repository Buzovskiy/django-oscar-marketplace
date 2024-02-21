import stripe
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Sum
from oscar.core.loading import get_class, get_model
from application.catalogue.models import Product

Order = get_model('order', 'Order')


class Command(BaseCommand):

    def handle(self, *args, **options):
        product_qs = Product.objects.filter(structure='parent').annotate(
            num_in_stock__sum=Sum('children__stockrecords__num_in_stock')
        ).filter(upc='R178637782 BK').get()
        # ).filter(upc='R737363736 BK').get()
        print(product_qs)
