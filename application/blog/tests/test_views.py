from django.test import TestCase
from oscar.core.loading import get_model
from django.urls import reverse
from django.conf import settings
from django.utils import translation

Post = get_model('blog', 'post')


class TestCaseCore(TestCase):
    fixtures = ['application/blog/fixtures/testing/blog.json']

    def setUp(self):
        for post in Post.objects.all()[:2]:
            post.status = 0
            post.save()


class BlogListViewTestCase(TestCaseCore):

    def test_list_view_url_exists_at_desired_location(self):
        resp = self.client.get(f"/{settings.LANGUAGE_CODE}/blog/")
        self.assertEqual(resp.status_code, 200)

    def test_list_view_url_accessible_by_name(self):
        translation.activate(settings.LANGUAGE_CODE)
        resp = self.client.get(reverse('blog:blog'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('active_label' in resp.context)
        self.assertEqual(resp.context['active_label'], '')


class BlogListViewSortedTestCase(TestCaseCore):

    def test_list_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/{settings.LANGUAGE_CODE}/blog/popular/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('active_label' in resp.context)
        self.assertEqual(resp.context['active_label'], 'popular')

        resp = self.client.get(f'/{settings.LANGUAGE_CODE}/blog/new/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('active_label' in resp.context)
        self.assertEqual(resp.context['active_label'], 'new')

    def test_list_view_url_accessible_by_name(self):
        translation.activate(settings.LANGUAGE_CODE)
        resp = self.client.get(reverse('blog:blog-sorted', args=['new']))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('blog:blog-sorted', args=['popular']))
        self.assertEqual(resp.status_code, 200)


class BlogListViewAllTestCase(TestCaseCore):

    def test_list_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/{settings.LANGUAGE_CODE}/blog/all/')
        self.assertEqual(resp.status_code, 200)

    def test_list_view_url_accessible_by_name(self):
        translation.activate(settings.LANGUAGE_CODE)
        resp = self.client.get(reverse('blog:blog-all'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('active_label' in resp.context)
        self.assertEqual(resp.context['active_label'], 'all')


class PostDetailViewTestCase(TestCaseCore):

    @property
    def object_to_test(self):
        return Post.objects.filter(status=1).first()

    def test_list_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/{settings.LANGUAGE_CODE}/blog/{self.object_to_test.slug}/')
        self.assertEqual(resp.status_code, 200)

    def test_list_view_url_accessible_by_name(self):
        translation.activate(settings.LANGUAGE_CODE)
        resp = self.client.get(reverse('blog:post-detail', args=[self.object_to_test.slug]))
        self.assertEqual(resp.status_code, 200)
