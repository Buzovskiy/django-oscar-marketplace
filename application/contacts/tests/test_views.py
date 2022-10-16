from django.test import TestCase
from django.urls import reverse
from django.conf import settings


class ContactsViewTestCase(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/{settings.LANGUAGE_CODE}/contacts/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('contacts:contacts'))
        self.assertEqual(resp.status_code, 200)


class BecomeOurPartnerViewTestCase(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/{settings.LANGUAGE_CODE}/contacts/become-our-partner')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('contacts:become-our-partner'))
        self.assertEqual(resp.status_code, 200)
