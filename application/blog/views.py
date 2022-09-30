from django.views.generic import ListView, DetailView
from oscar.core.loading import get_model
from django.urls import reverse

Post = get_model('blog', 'post')
posts_on_page = 6


class BlogListCore(ListView):
    model = Post

    def get_queryset(self):
        return self.model.published.all()


class BlogListView(BlogListCore):
    paginate_by = posts_on_page

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogListView, self).get_context_data()
        context['page_url'] = reverse('blog:blog')
        context['active_label'] = ''
        return context


class BlogListViewSorted(BlogListView):

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['page_url'] = reverse('blog:blog-sorted', args=[self.kwargs['sorting']])
        context['active_label'] = self.kwargs['sorting']
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs['sorting'] == 'popular':
            queryset = queryset.order_by('popularity')
        elif self.kwargs['sorting'] == 'new':
            queryset = queryset.order_by('-created_on')
        return queryset


class BlogListViewAll(BlogListCore):
    model = Post
    context_object_name = 'page_obj'
    template_name = 'blog/post_list_all.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['active_label'] = 'all'
        return context


class PostDetailView(DetailView):
    model = Post

    def get_queryset(self):
        return self.model.published.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['also_read_posts'] = self.model.published.all().exclude(pk=context['object'].id).order_by('?')[:2]
        return context
