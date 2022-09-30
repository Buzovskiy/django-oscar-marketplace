from django.test import TestCase
from django.urls import reverse


class ContactsViewTestCase(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/contacts/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('contacts:contacts'))
        self.assertEqual(resp.status_code, 200)


class BecomeOurPartnerViewTestCase(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/contacts/become-our-partner')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('contacts:become-our-partner'))
        self.assertEqual(resp.status_code, 200)
