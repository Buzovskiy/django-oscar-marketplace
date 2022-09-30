# python manage.py test application.home.tests.test_models

import shutil
from django.test import TestCase, override_settings
from application.home.models import HomeBanner
from django.conf import settings
from django.core.files.base import File
from pathlib import Path


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'media-test')
class HomeBannerTestCase(TestCase):

    image_left_path = settings.BASE_DIR / 'application/home/fixtures/sample_files_for_testing/accessories-1.jpg'
    image_right_path = settings.BASE_DIR / 'application/home/fixtures/sample_files_for_testing/accessories-2.jpg'

    def setUp(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        self.create_banner()

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        self.remove_banners()

    def create_banner(self):
        self.banner = HomeBanner.objects.create()
        with open(self.image_left_path, mode='rb') as f:
            self.banner.image_left.save('image_left.jpg', File(f))
        with open(self.image_right_path, mode='rb') as f:
            self.banner.image_right.save('image_right.jpg', File(f))

    @classmethod
    def remove_banners(cls):
        for banner in HomeBanner.objects.all():
            banner.delete()

    def test_image_left_upload_to(self):
        self.assertEqual(self.banner._meta.get_field('image_left').upload_to, 'images/home-banners/')

    def test_image_right_upload_to(self):
        self.assertEqual(self.banner._meta.get_field('image_right').upload_to, 'images/home-banners/')

    def test_save(self):
        banner = HomeBanner.objects.get()
        self.assertEqual('homeBannerIdSelector1', banner.section_id_selector)
