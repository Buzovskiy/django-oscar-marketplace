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
Range = get_model('offer', 'Range')
RangeProduct = get_model('offer', 'RangeProduct')
Benefit = get_model('offer', 'Benefit')
from application.partner.models import RetailCity


class Command(BaseCommand):
    def handle(self, **options):
        qs = Product.objects.filter(upc='R800456351 DB')
        qs = qs.prefetch_related('rangeproduct_set__range__benefit_set')
        # qs = qs.select_related('rangeproduct_set__range')
        for product in qs.all():
            print(product.id)
            for range_product in product.rangeproduct_set.all():
                range = range_product.range
        # qs = RangeProduct.objects.all()
        # qs = qs.select_related('range')
        # for range_product in qs:
        #     range = range_product.range
        #     print(range.id)
        print(connection.queries)
