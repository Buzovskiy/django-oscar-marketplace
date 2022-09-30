from oscar.core.application import OscarConfig
from django.urls import path, re_path
from oscar.core.loading import get_class


class BlogConfig(OscarConfig):
    blog_list_view = blog_post_detail_view = blog_list_view_sorted = blog_list_view_all = None
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'blog'
    name = 'application.blog'
    namespace = 'blog'

    def ready(self):
        self.blog_list_view = get_class('blog.views', 'BlogListView')
        self.blog_list_view_all = get_class('blog.views', 'BlogListViewAll')
        self.blog_list_view_sorted = get_class('blog.views', 'BlogListViewSorted')
        self.blog_post_detail_view = get_class('blog.views', 'PostDetailView')

    def get_urls(self):
        urls = [
            path('blog/', self.blog_list_view.as_view(), name='blog'),
            path('blog/all/', self.blog_list_view_all.as_view(), name='blog-all'),  # show all posts
            re_path(
                r'blog/(?P<sorting>(?:(popular|new)))/$',
                self.blog_list_view_sorted.as_view(),
                name='blog-sorted'  # sort by popularity or created_on
            ),
            path('blog/<slug:slug>/', self.blog_post_detail_view.as_view(), name='post-detail'),
        ]
        return self.post_process_urls(urls)
