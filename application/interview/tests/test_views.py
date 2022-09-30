"""
Run tests: python manage.py test application.interview.tests.test_views
"""

from django.test import TestCase


class InterviewViewTestCase(TestCase):
    """test application.interview.tests.test_views.InterviewViewTestCase"""

    def test_view_urls_exist_at_desired_location(self):

        resp1 = self.client.get('/interview/start/')
        self.assertEqual(resp1.status_code, 200)

        resp1 = self.client.get('/interview/stage-01/')
        self.assertEqual(resp1.status_code, 200)

        resp1 = self.client.get('/interview/stage-02/')
        self.assertEqual(resp1.status_code, 200)

        resp1 = self.client.get('/interview/stage-03/')
        self.assertEqual(resp1.status_code, 200)

        resp1 = self.client.get('/interview/stage-04/')
        self.assertEqual(resp1.status_code, 200)

        resp1 = self.client.get('/interview/stage-05/')
        self.assertEqual(resp1.status_code, 200)
