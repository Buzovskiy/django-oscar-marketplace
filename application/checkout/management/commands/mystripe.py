import stripe
from django.core.management.base import BaseCommand
from django.conf import settings
from oscar.core.loading import get_class, get_model

Order = get_model('order', 'Order')


class Command(BaseCommand):

    def handle(self, *args, **options):
        order = Order.objects.filter(pk=16).get()
        # this command does nothing
