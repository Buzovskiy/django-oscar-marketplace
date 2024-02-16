from django.core.management.base import BaseCommand

import re
import os
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from oscar.core.loading import get_class, get_classes, get_model
import xml.etree.ElementTree as ET
from slugify import slugify_filename
from application.catalogue.utils import get_sizes_list_from_range

from django.db import connection


ProductClass = get_model('catalogue', 'ProductClass')
ProductAttribute = get_model('catalogue', 'ProductAttribute')
ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
Category = get_model('catalogue', 'Category')
Product = get_model('catalogue', 'Product')
ProductRecommendation = get_model('catalogue', 'ProductRecommendation')
ProductImage = get_model('catalogue', 'ProductImage')
ColorHexCode = get_model('catalogue', 'ColorHexCode')
Partner = get_model('partner', 'Partner')
StockRecord = get_model('partner', 'StockRecord')
from application.partner.models import RetailCity


class Command(BaseCommand):
    def handle(self, **options):
        from django.db.models import Sum
        # qs = Product.objects.filter(structure='parent').annotate(
        #     num_in_stock__sum=Sum('children__stockrecords__num_in_stock')
        # )
        # for product in qs:
        #     if product.num_in_stock__sum == 0:
        #         product.is_public = False
        #     else:
        #         product.is_public = True
        print(connection.queries)
