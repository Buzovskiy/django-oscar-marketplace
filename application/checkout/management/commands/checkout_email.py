import stripe
from django.template.loader import render_to_string
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Sum
from oscar.core.loading import get_class, get_model
from application.catalogue.models import Product

Order = get_model('order', 'Order')


class Command(BaseCommand):

    def handle(self, *args, **options):
        order = Order.objects.filter(pk=71).first()
        res = render_to_string(
            template_name='oscar/communication/emails/commtype_order_placed_body_simple.html',
            context={'order': order}
        )
        print(res)
