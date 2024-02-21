import re
import os
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import Sum
from oscar.core.loading import get_class, get_classes, get_model
from .files import FileXml, FileImage
import xml.etree.ElementTree as ET
from slugify import slugify_filename
from application.catalogue.utils import get_sizes_list_from_range

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


class ImportImage:
    file_obj = None

    def __init__(self, file_name):
        """
        :param file_name: name of the file. The same as file_name in FileCore class
        """
        self.file_obj = FileImage(file_name)

    def save_product_image(self):
        name_parts = self.file_obj.get_name_parts()
        if name_parts is None:
            return False
        else:
            external_id, display_order = name_parts

        try:
            product = Product.objects.filter(structure='parent', external_id=external_id).get()
        except ObjectDoesNotExist:
            return False

        with open(self.file_obj.full_path, 'rb') as original_img:
            with ContentFile(original_img.read()) as new_image:
                try:
                    product_image = ProductImage.objects.filter(product=product, display_order=display_order).get()
                except ObjectDoesNotExist:
                    product_image = ProductImage(product=product, display_order=display_order)
                product_image.original.save(os.path.basename(self.file_obj.full_path), new_image)
                product_image.save()  # Save object

    def clean(self):
        """Remove image when exchange is done"""
        if self.file_obj is not None:
            self.file_obj.remove()


class ImportCore:
    xml_root = file_obj = None

    def __init__(self, file_name=None):
        """
        :param file_name: name of the file. The same as file_name in FileCore class
        """
        if file_name is not None:
            self.file_obj = FileXml(file_name)
            xml_tree = ET.parse(self.file_obj.full_path)
            self.xml_root = xml_tree.getroot()

    def clean(self):
        """Remove exchange file when exchange is done"""
        if self.file_obj is not None:
            self.file_obj.remove()


class ImportProduct(ImportCore):

    @staticmethod
    def save_product_class():
        ProductClass.objects.update_or_create(
            slug=settings.PRODUCT_CLASS_SHOES_SLUG,
            defaults={'name': 'Shoes'},
        )

    @staticmethod
    def save_default_partner():
        Partner.objects.update_or_create(
            code=settings.PARTNER_DEFAULT['code'],
            defaults={
                'name': settings.PARTNER_DEFAULT['name']
            }
        )

    def save_categories(self):
        for category_xml in self.xml_root.findall("./Классификатор/Группы/Группа/Группы/Группа"):
            external_id_xml = category_xml.find('Ид').text
            name_xml = category_xml.find('Наименование').text
            category_obj = Category.objects.filter(external_id=external_id_xml)
            if category_obj.count() == 1:
                category_obj.update(name=name_xml)
            elif not category_obj.count():
                Category.add_root(name=name_xml, external_id=external_id_xml)

    def save_attributes(self):
        attributes_excluded = ['Цифры']
        try:
            product_class = ProductClass.objects.filter(name='Shoes').get()
        except ObjectDoesNotExist:
            pass
        else:
            for attribute_xml in self.xml_root.findall('./Классификатор/Свойства/СвойствоНоменклатуры'):
                name_xml = attribute_xml.find('Наименование').text

                if name_xml in attributes_excluded:
                    continue

                external_id_xml = attribute_xml.find('Ид').text
                attribute = ProductAttribute.objects.filter(
                    product_class=product_class,
                    external_id=external_id_xml
                )
                if not attribute.count():
                    name_xml = attribute_xml.find('Наименование').text
                    products_attribute = ProductAttribute(
                        product_class=product_class,
                        name=name_xml,
                        code=slugify_filename(name_xml, to_lower=True).replace("-", "_"),
                        external_id=external_id_xml,
                        type='text',
                    )
                    products_attribute.full_clean()
                    products_attribute.save()

            # Save extra attributes that does not exist in xml file
            ProductAttribute.objects.update_or_create(
                code='size',
                product_class=product_class,
                defaults={'name': 'Size', 'type': 'text'},
            )
            ProductAttribute.objects.update_or_create(
                code='color_hex_code',
                product_class=product_class,
                defaults={'name': 'Color hex code', 'type': 'text'},
            )

    def save_products(self):
        for product_xml in self.xml_root.findall('./Каталог/Товары/Товар'):
            external_id_xml_parts_list = product_xml.find('Ид').text.split('#')

            if len(external_id_xml_parts_list) == 1:
                self.save_product_parent(product_xml=product_xml)
            elif len(external_id_xml_parts_list) == 2:
                self.save_product_children(product_xml=product_xml)

    def save_product_parent(self, product_xml):
        """product.title, see .models.product_category_changed"""
        product_class = ProductClass.objects.filter(name='Shoes').get()
        external_id_xml = product_xml.find('Ид').text
        try:
            category_external_id_xml = product_xml.find('./Группы/Ид').text
        except AttributeError:
            return False

        try:
            category = Category.objects.filter(external_id=category_external_id_xml).get()
        except ObjectDoesNotExist:
            return False

        try:
            status_xml = product_xml.find('./Статус').text
        except AttributeError:
            pass
        else:
            if status_xml == 'Удален':
                try:
                    Product.objects.filter(external_id=external_id_xml).get().delete()
                except ObjectDoesNotExist:
                    pass
                return False  # If see product with Удален status, skip it

        upc_xml = product_xml.find('Артикул').text
        # If find product with the same upc but different external_id delete it
        try:
            Product.objects.exclude(external_id=external_id_xml).filter(upc=upc_xml).get().delete()
        except ObjectDoesNotExist:
            pass

        product, created = Product.objects.update_or_create(
            external_id=external_id_xml, upc=upc_xml,
            defaults={
                'structure': 'parent',
                'upc': upc_xml,
                'product_class': product_class,
            },
        )

        # Add category to product
        product.categories.add(category)
        product.full_clean()

        # Save product attributes values
        for product_attribute_xml in product_xml.findall('./ЗначенияСвойств/ЗначенияСвойства'):
            attribute_external_id_xml = product_attribute_xml.find('Ид').text
            try:
                attribute = ProductAttribute.objects.filter(external_id=attribute_external_id_xml).get()
            except ObjectDoesNotExist:
                continue

            try:
                product_attribute_xml.find('Значение').text
            except AttributeError:
                continue

            if not product_attribute_xml.find('Значение').text:
                continue

            try:
                product_attribute_value, created = ProductAttributeValue.objects.update_or_create(
                    attribute=attribute, product=product,
                    defaults={
                        'value_text': product_attribute_xml.find('Значение').text
                    },
                )
            except ValidationError:
                continue

            if attribute.code == settings.ATTR_COLOR_CODE:  # if tsvet
                ColorHexCode.objects.update_or_create(
                    color=product_attribute_value.value_text,
                )

        self.save_color_hex_code_product_attribute(product)

    @staticmethod
    def save_product_children(product_xml):
        """Save product children according to product size variations"""
        external_id_xml = product_xml.find('Ид').text
        parent_external_id_xml = external_id_xml.split('#')[0]

        try:
            product_parent = Product.objects.filter(external_id=parent_external_id_xml).get()
        except ObjectDoesNotExist:
            return False

        size_xml = None
        for product_attribute_xml in product_xml.findall('./ЗначенияСвойств/ЗначенияСвойства'):
            attribute_external_id_xml = product_attribute_xml.find('Ид').text

            if attribute_external_id_xml != 'property_razmer':
                continue

            try:
                ProductAttribute.objects.filter(external_id=attribute_external_id_xml).get()
            except ObjectDoesNotExist:
                continue

            try:
                product_attribute_xml.find('Значение').text
            except AttributeError:
                continue

            if not re.match(r'^\d{2}$', product_attribute_xml.find('Значение').text):
                continue

            size_xml = product_attribute_xml.find('Значение').text

        if not size_xml:
            return False

        try:
            product_child = Product.objects.filter(
                parent=product_parent, external_id=external_id_xml
            ).get()
        except ObjectDoesNotExist:
            product_child = Product()

        product_child.structure = 'child'
        product_child.external_id = external_id_xml
        product_child.parent = product_parent
        product_child.upc = f"{product_parent.upc}: {size_xml}"
        product_child.title = f"{product_parent.title} | {_('Size')} {size_xml}"
        product_child.custom_save()
        product_child.full_clean()

        # save child product size attribute value
        try:
            size_attribute = ProductAttribute.objects.filter(code='size').get()
            ProductAttributeValue.objects.update_or_create(
                attribute=size_attribute, product=product_child,
                defaults={'value_text': size_xml},
            )
        except (ObjectDoesNotExist, ValidationError):
            return False


    @staticmethod
    def save_color_hex_code_product_attribute(product):
        """
        Save color_hex_code_attribute separately, as it does not exist in xml file
        """
        try:  # Get color of a product
            color = ProductAttributeValue.objects.filter(
                attribute__code=settings.ATTR_COLOR_CODE, product=product).get().value_text
        except ObjectDoesNotExist:
            return False
        try:  # Look for color hex code in ColorHexCode table
            color_hex_code = ColorHexCode.objects.filter(color=color).get().hex_code
        except ObjectDoesNotExist:
            return False

        # If there is no color hex code in ColorHexCode, set white color code by default
        color_hex_code = color_hex_code or '#ffffff'

        ProductAttributeValue.objects.update_or_create(
            attribute=ProductAttribute.objects.filter(code="color_hex_code").get(), product=product,
            defaults={'value_text': color_hex_code}
        )

    @staticmethod
    def save_recommended():
        # Delete all recommendations
        ProductRecommendation.objects.all().delete()

        products = Product.objects.filter(
            structure='parent', product_class__slug=settings.PRODUCT_CLASS_SHOES_SLUG).all()
        for product in products:
            upc_reg_match = re.search(r'^([a-zA-Z0-9]+)\s[a-zA-z0-9]+$', product.upc)
            if upc_reg_match is None:
                continue
            product_upc_beginning = upc_reg_match.group(1)
            for product_rec in products:
                if product_rec.id == product.id:
                    continue
                product_rec_upc_reg_math = re.search(r'^([a-zA-Z0-9]+)\s[a-zA-z0-9]+$', product_rec.upc)
                if product_rec_upc_reg_math is None:
                    continue
                product_rec_upc_beginning = product_rec_upc_reg_math.group(1)
                if product_upc_beginning != product_rec_upc_beginning:
                    continue
                product.recommended_products.add(product_rec)


class ImportOffers(ImportCore):

    def save_stock_records(self):
        offers = self.xml_root.findall('./ПакетПредложений/Предложения/Предложение')
        for offer_xml in offers:
            try:
                price = offer_xml.find('./Цены/Цена/ЦенаЗаЕдиницу').text
            except AttributeError:
                continue

            external_id_xml = offer_xml.find('Ид').text
            if len(external_id_xml.split('#')) != 2:
                continue

            try:  # try finding product and partner. If not found, go to another one
                product = Product.objects.filter(
                    structure='child',
                    external_id=external_id_xml,
                ).get()
                partner = Partner.objects.filter(code=settings.PARTNER_DEFAULT['code']).get()
            except ObjectDoesNotExist:
                continue

            # If quantity below 0, turn it into 0
            num_in_stock_xml = float(offer_xml.find('Количество').text)
            num_in_stock_xml = num_in_stock_xml if num_in_stock_xml > 0 else 0

            product.is_public = False if num_in_stock_xml == 0 else True
            product.save()

            try:
                StockRecord.objects.update_or_create(
                    partner=partner, product=product,
                    defaults={
                        'partner_sku': f'{product.upc} | {partner.name}',
                        'price': float(price),
                        'num_in_stock': num_in_stock_xml,
                    })
            except ValueError:
                continue

        product_qs = Product.objects.filter(structure='parent').annotate(
            num_in_stock__sum=Sum('children__stockrecords__num_in_stock')
        )
        for product in product_qs:
            product.is_public = False if product.num_in_stock__sum == 0 else True
            product.save()
