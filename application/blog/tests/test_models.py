from django.test import TestCase
from oscar.core.loading import get_model

Post = get_model('blog', 'post')


class BlogModelsTestCase(TestCase):
    fixtures = ['application/blog/fixtures/testing/blog.json']

    def setUp(self):
        for post in Post.objects.all()[:2]:
            post.status = 0
            post.save()

    def test_published_posts(self):
        published = Post.published.all()
        self.assertEqual(published.filter(status=0).count(), 0)
