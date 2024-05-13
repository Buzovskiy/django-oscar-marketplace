"""
python manage.py test application.exchange.tests.test_import_product --noinput
"""
import shutil
import xml.etree.ElementTree as ET
from .fixtures import fixtures
from django.conf import settings
from django.test import TestCase, TransactionTestCase, override_settings
from ..onec import ImportProduct, ImportOffers, ImportImage
from oscar.core.loading import get_class, get_classes, get_model
from ..files import FileXml, FileImage
ProductClass = get_model('catalogue', 'ProductClass')
ProductAttribute = get_model('catalogue', 'ProductAttribute')
Category = get_model('catalogue', 'Category')
Partner = get_model('partner', 'Partner')
from application.catalogue.models import Filter


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'media-test')
class ImportProductTest(TransactionTestCase):
    """
    python manage.py test application.exchange.tests.test_import_product.ImportProductTest --noinput
    """

    def setUp(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        shutil.copy(fixtures['import.xml'], settings.MEDIA_ROOT / FileXml().upload_to / 'import.xml')
        file_obj = FileXml('import.xml')
        xml_tree = ET.parse(file_obj.full_path)
        self.xml_root = xml_tree.getroot()

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT)
        # input(
        #     'Execution is paused and you can now inspect the database.\n'
        #     'Press return/enter key to continue:')

    def test_class(self):
        """
        python manage.py test application.exchange.tests.test_import_product.ImportProductTest.test_class --keepdb
        """
        ImportProduct('import.xml').save_product_class()
        self.assertEqual(ProductClass.objects.filter(name='Shoes').count(), 1)

    def test_save_categories(self):
        """
        python manage.py test application.exchange.tests.test_import_product.ImportProductTest.test_save_categories --keepdb
        """
        ImportProduct('import.xml').save_categories()
        categories_count = len(self.xml_root.findall("./Классификатор/Группы/Группа/Группы/Группа"))
        self.assertEqual(Category.objects.all().count(), categories_count)
        ImportProduct('import.xml').save_categories()
        self.assertEqual(Category.objects.all().count(), categories_count)

    def test_save_attributes(self):
        """
        python manage.py test application.exchange.tests.test_import_product.ImportProductTest.test_save_attributes --keepdb
        """
        import_xml_inst = ImportProduct('import.xml')
        import_xml_inst.save_product_class()
        import_xml_inst.save_attributes()

    def test_save_products(self):
        """
        python manage.py test application.exchange.tests.test_import_product.ImportProductTest.test_save_products --keepdb
        """
        import_xml_inst = ImportProduct('import.xml')
        import_xml_inst.save_product_class()
        import_xml_inst.save_categories()
        import_xml_inst.save_attributes()
        import_xml_inst.save_products()

    def test_save_recommended(self):
        """
        python manage.py test application.exchange.tests.test_import_product.ImportProductTest.test_save_recommended --keepdb
        """
        import_xml_inst = ImportProduct('import.xml')
        import_xml_inst.save_product_class()
        import_xml_inst.save_categories()
        import_xml_inst.save_attributes()
        import_xml_inst.save_products()
        import_xml_inst.save_recommended()

    def test_save_default_partner(self):
        """
        python manage.py test application.exchange.tests.test_import_product.ImportProductTest.test_save_default_partner --keepdb
        """
        import_xml_inst = ImportProduct('import.xml')
        import_xml_inst.save_default_partner()
        import_xml_inst.save_default_partner()
        self.assertEqual(
            Partner.objects.filter(code=settings.PARTNER_DEFAULT['code']).count(), 1)


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'media-test')
class ImportOffersTest(TransactionTestCase):
    """
    python manage.py test application.exchange.tests.test_import_product.ImportOffersTest --noinput
    """

    def setUp(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        shutil.copy(fixtures['offers.xml'], settings.MEDIA_ROOT / FileXml().upload_to / 'offers.xml')
        shutil.copy(fixtures['import.xml'], settings.MEDIA_ROOT / FileXml().upload_to / 'import.xml')

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT)
        # input(
        #     'Execution is paused and you can now inspect the database.\n'
        #     'Press return/enter key to continue:')

    def test_save_stock_records(self):
        """
        python manage.py test application.exchange.tests.test_import_product.ImportOffersTest.test_save_stock_records --keepdb
        """
        import_xml_inst = ImportProduct('import.xml')
        import_xml_inst.save_default_partner()
        import_xml_inst.save_product_class()
        import_xml_inst.save_product_class()
        import_xml_inst.save_categories()
        import_xml_inst.save_attributes()
        import_xml_inst.save_products()
        ImportOffers('offers.xml').save_stock_records()


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'media-test')
class ImportImageTest(TransactionTestCase):
    """
    python manage.py test application.exchange.tests.test_import_product.ImportImageTest --noinput
    """

    def setUp(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        image_name = '3cb3474f-d9a8-11e9-81dc-2c4d5446690f'
        shutil.copy(fixtures[f'{image_name}.jpg'], FileImage(f'{image_name}.jpg').full_path)
        shutil.copy(fixtures[f'{image_name}_1.jpg'], FileImage(f'{image_name}_1.jpg').full_path)
        shutil.copy(fixtures[f'{image_name}_2.jpg'], FileImage(f'{image_name}_2.jpg').full_path)
        shutil.copy(fixtures['offers.xml'], settings.MEDIA_ROOT / FileXml().upload_to / 'offers.xml')
        shutil.copy(fixtures['import.xml'], settings.MEDIA_ROOT / FileXml().upload_to / 'import.xml')

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT)
        # input(
        #     'Execution is paused and you can now inspect the database.\n'
        #     'Press return/enter key to continue:')

    def test_save_product_image(self):
        """
        python manage.py test application.exchange.tests.test_import_product.ImportImageTest.test_save_product_image --keepdb
        """
        import_xml_inst = ImportProduct('import.xml')
        import_xml_inst.save_default_partner()
        import_xml_inst.save_product_class()
        import_xml_inst.save_product_class()
        import_xml_inst.save_categories()
        import_xml_inst.save_attributes()
        import_xml_inst.save_products()
        ImportOffers('offers.xml').save_stock_records()
        import_image_inst = ImportImage('3cb3474f-d9a8-11e9-81dc-2c4d5446690f.jpg')
        import_image_inst.save_product_image()


# class FilterTest(TransactionTestCase):
#     def test_save_filters(self):
#         save_filters()
#         for key, facet in settings.OSCAR_SEARCH_FACETS['fields'].items():
#             count = Filter.objects.filter(field=key).count()
#             self.assertEqual(1, count)
