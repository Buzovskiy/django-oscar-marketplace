"""
Run tests: python manage.py test application.exchange.tests.test_views
"""
from django.test import SimpleTestCase
from django.conf import settings
from django.test import override_settings
from pathlib import Path
import shutil
from ..files import FileXml, FileImage
import xml.etree.ElementTree as ET
from .fixtures import fixtures


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'media-test')
class TestCaseCore(SimpleTestCase):

    def setUp(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def tearDown(self):
        # Remove image exchange directory
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)


class ExchangeViewTestCase(TestCaseCore):

    def test_view_url_exists_at_desired_location(self):
        """
        test application.exchange.tests.test_views.ExchangeViewTestCase.test_view_url_exists_at_desired_location
        """
        url_tested = '/1c_exchange/?mode=checkauth'

        resp = self.client.get(url_tested)
        self.assertEqual(resp.status_code, 200, msg=url_tested)
        self.assertEqual(
            resp.content.decode('utf-8'),
            'success\n', msg=f"{url_tested}: no success message")

    def test_import_xml_save_part(self):
        """
        python manage.py test application.exchange.tests.test_views.ExchangeViewTestCase.test_import_xml_save_part
        """
        url_tested = '/1c_exchange/?type=catalog&mode=file&filename=import.xml'
        for i in [0, 1]:
            with open(fixtures[f'import.xml.part{i}'], 'rb') as f:
                content = f.read()
                resp = self.client.generic(
                    method='POST',
                    path=url_tested,
                    data=content)
                self.assertEqual(resp.status_code, 200, msg=url_tested)
                path_to_file = FileXml(f'import.xml.part{i}').full_path
                self.assertTrue(path_to_file.exists())

    def test_import_xml_make_file(self):
        """
        python manage.py test application.exchange.tests.test_views.ExchangeViewTestCase.test_import_xml_make_file
        """
        url_tested = '/1c_exchange/?type=catalog&mode=import&filename=import.xml'
        self.test_import_xml_save_part()

        resp = self.client.get(url_tested)
        self.assertEqual(resp.status_code, 200, msg=url_tested)
        self.assertEqual(
            resp.content.decode('utf-8'),
            'success\n', msg=f"{url_tested}: no success message")
        file = FileXml('import.xml')
        self.assertTrue(file.full_path.exists(), msg='No file import.xml')
        # Try to parse xml
        ET.parse(file.full_path)

    def test_save_image(self):
        """
        python manage.py test application.exchange.tests.test_views.ExchangeViewTestCase.test_save_image
        """
        url_tested = '/1c_exchange/?type=catalog&mode=file&filename=import_files/05/3cb3474f-d9a8-11e9-81dc' \
                     '-2c4d5446690f.jpg'
        with open(fixtures['3cb3474f-d9a8-11e9-81dc-2c4d5446690f.jpg'], 'rb') as f:
            content = f.read()
        resp = self.client.generic(
            method='POST',
            path=url_tested,
            data=content)
        self.assertEqual(resp.status_code, 200, msg=url_tested)
        self.assertEqual(resp.content.decode('utf-8'), 'success\n', msg=f"{url_tested}: no success message")
        path_to_file = FileImage('3cb3474f-d9a8-11e9-81dc-2c4d5446690f.jpg').full_path
        self.assertTrue(Path(path_to_file).exists())
