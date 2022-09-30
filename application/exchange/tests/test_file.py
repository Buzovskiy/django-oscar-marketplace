"""
Run tests: python manage.py test application.exchange.tests.test_file
"""
from pathlib import Path
import shutil
import sys
import os
import xml.etree.ElementTree as ET
from django.test import SimpleTestCase, override_settings
from django.conf import settings
from ..files import FileImage, FileXml, get_images_list
from .fixtures import fixtures


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'media-test')
class TestCaseFileImage(SimpleTestCase):
    """
    Run test: python manage.py test application.exchange.tests.test_file.TestCaseFileImage
    """

    def setUp(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def tearDown(self):
        # Remove image exchange directory
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_get_name_parts(self):
        """
        python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_get_name_parts
        """
        file_name = '3cb3474f-d9a8-11e9-81dc-2c4d5446690f.jpg'
        file_obj = FileImage(file_name)
        shutil.copy(fixtures[file_name], Path(settings.MEDIA_ROOT / file_obj.upload_to))
        self.assertEqual(file_obj.get_name_parts(), ('3cb3474f-d9a8-11e9-81dc-2c4d5446690f', 0))

        file_name = '3cb3474f-d9a8-11e9-81dc-2c4d5446690f_1.jpg'
        file_obj = FileImage(file_name)
        shutil.copy(fixtures[file_name], Path(settings.MEDIA_ROOT / file_obj.upload_to))
        self.assertEqual(file_obj.get_name_parts(), ('3cb3474f-d9a8-11e9-81dc-2c4d5446690f', 1))

    def test_is_image(self):
        """
        Run: python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_is_image
        """
        file_name = '3cb3474f-d9a8-11e9-81dc-2c4d5446690f.jpg'
        file_obj = FileImage(file_name)
        shutil.copy(fixtures[file_name], Path(settings.MEDIA_ROOT / file_obj.upload_to))
        self.assertTrue(file_obj.is_image)
        file_name = 'import.xml'
        file_obj = FileImage(file_name)
        shutil.copy(fixtures[file_name], Path(settings.MEDIA_ROOT / file_obj.upload_to))
        self.assertFalse(file_obj.is_image)

    def test_file_image_init(self):
        """
        Run: python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_file_image_init
        """
        file_obj = FileImage('some-image.jpg')
        self.assertTrue(Path(settings.MEDIA_ROOT / '1c/temp/images/').is_dir())
        self.assertEqual(file_obj.full_path, settings.MEDIA_ROOT / '1c/temp/images/some-image.jpg')
        self.assertEqual(file_obj.relative_path, Path('1c/temp/images/some-image.jpg'))
        self.assertEqual(settings.BASE_DIR / file_obj.upload_to, settings.BASE_DIR / '1c/temp/images')

    def test_image_save_file(self):
        """
        Run: python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_image_save_file
        """
        file_name = '3cb3474f-d9a8-11e9-81dc-2c4d5446690f.jpg'
        with open(fixtures[file_name], mode='rb') as f:
            content = f.read()
        file_obj = FileImage(file_name)
        file_obj.save_file(content=content)
        self.assertTrue(Path(file_obj.full_path).exists())

    def test_file_xml_init(self):
        """
        Run: python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_file_xml_init
        """
        file_obj = FileXml('import.xml')
        self.assertTrue(Path(settings.MEDIA_ROOT / '1c/temp/xml/').is_dir())
        self.assertEqual(file_obj.full_path, settings.MEDIA_ROOT / '1c/temp/xml/import.xml')
        self.assertEqual(file_obj.relative_path, Path('1c/temp/xml/import.xml'))
        self.assertEqual(settings.BASE_DIR / file_obj.upload_to, settings.BASE_DIR / '1c/temp/xml/')

    def test_file_xml_save_part(self):
        """
        Run: python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_file_xml_save_part
        """
        file_obj = FileXml()
        for i in [0, 1]:
            with open(fixtures[f'import.xml.part{i}'], 'rb') as f:
                content = f.read()
                file_obj.save_part(filename='import.xml', content=content)
                self.assertTrue(Path(settings.MEDIA_ROOT / file_obj.upload_to / f'import.xml.part{i}'))

    def test_remove_xml(self):
        """
        Run: python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_remove_xml
        """
        file_obj = FileXml('import.xml')
        file_obj.remove()
        self.assertFalse(Path(file_obj.full_path).exists())
        shutil.copy(fixtures['import.xml'], Path(settings.MEDIA_ROOT / file_obj.upload_to))
        self.assertTrue(Path(file_obj.full_path).exists())
        file_obj.remove()
        self.assertFalse(Path(file_obj.full_path).exists())

    def test_remove_image(self):
        """
        Run: python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_remove_image
        """
        file_obj = FileImage('3cb3474f-d9a8-11e9-81dc-2c4d5446690f.jpg')
        file_obj.remove()
        self.assertFalse(Path(file_obj.full_path).exists())
        shutil.copy(
            fixtures['3cb3474f-d9a8-11e9-81dc-2c4d5446690f.jpg'], Path(settings.MEDIA_ROOT / file_obj.upload_to))
        self.assertTrue(Path(file_obj.full_path).exists())
        file_obj.remove()
        self.assertFalse(Path(file_obj.full_path).exists())

        shutil.copytree(fixtures['image-files'], settings.MEDIA_ROOT / file_obj.upload_to, dirs_exist_ok=True)
        file_obj = FileImage('import_files/4c/3cb3474f-d9a8-11e9-81dc-2c4d5446690f.jpg')
        self.assertTrue(file_obj.full_path.exists())
        file_obj.remove()
        self.assertFalse(file_obj.full_path.exists())
        self.assertFalse(file_obj.full_path.parent.exists())

    def test_remove_empty_dirs(self):
        """
        Run: python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_remove_empty_dirs
        """
        file_obj = FileImage()
        Path(settings.MEDIA_ROOT / file_obj.upload_to / 'dir1/dir11-11').mkdir(parents=True, exist_ok=True)
        Path(settings.MEDIA_ROOT / file_obj.upload_to / 'dir1/dir11/dir111').mkdir(parents=True, exist_ok=True)
        Path(settings.MEDIA_ROOT / file_obj.upload_to / 'dir2/dir22/dir222').mkdir(parents=True, exist_ok=True)
        self.assertTrue(Path(settings.MEDIA_ROOT / file_obj.upload_to / 'dir2/dir22/dir222').exists())
        with open(Path(settings.MEDIA_ROOT / file_obj.upload_to / 'dir2/dir22/dir222/222.txt'), mode='w'):
            pass

        file_obj.remove_empty_dirs()
        self.assertTrue(Path(settings.MEDIA_ROOT / file_obj.upload_to / 'dir2/dir22/dir222/222.txt'))
        self.assertTrue(Path(settings.MEDIA_ROOT / file_obj.upload_to / 'dir2/dir22/').exists())
        self.assertFalse(Path(settings.MEDIA_ROOT / file_obj.upload_to / 'dir1/dir11-11').exists())
        self.assertFalse(Path(settings.MEDIA_ROOT / file_obj.upload_to / 'dir1/dir11/dir111').exists())

    def test_make_file_two_parts(self):
        """
        python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_make_file_two_parts
        """
        self.test_file_xml_save_part()
        FileXml().make_file('import.xml')
        file = FileXml('import.xml')
        ET.parse(file.full_path)

    def test_make_file_one_part(self):
        """
        python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_make_file_one_part
        """
        shutil.copy(fixtures['import.xml'], settings.MEDIA_ROOT / FileXml().upload_to / 'import.xml.part0')
        self.assertTrue(FileXml('import.xml.part0').full_path.exists())
        FileXml().make_file('import.xml')
        file = FileXml('import.xml')
        self.assertTrue(file.full_path.exists())
        ET.parse(file.full_path)

    def test_get_images_list(self):
        """
        Run: python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_get_images_list
        """
        image_obj = FileImage()
        shutil.copytree(fixtures['image-files'], settings.MEDIA_ROOT / image_obj.upload_to, dirs_exist_ok=True)
        self.assertTrue(len(get_images_list()) > 0)

    def test_get_images_list_empty(self):
        """
        python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_get_images_list_empty
        """
        image_obj = FileImage()
        self.assertTrue(len(get_images_list()) == 0)

    def test_url(self):
        """
        python manage.py test application.exchange.tests.test_file.TestCaseFileImage.test_url
        """
        obj = FileImage('import_files/ps/some-image.jpg')
        print(obj.url)
        self.assertEqual(settings.MEDIA_URL + '1c/temp/images/import_files/ps/some-image.jpg', obj.url)
