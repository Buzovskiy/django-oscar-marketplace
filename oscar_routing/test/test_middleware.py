from django.test import TestCase


class AccessSiteTestCase(TestCase):
    """
    Running tests:
    python manage.py test oscar_routing.test.test_middleware
    """

    def test_access(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        with self.settings(BLOCKED_IPS='127.0.0.1'):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 403)
