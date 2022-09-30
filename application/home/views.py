from django.views.generic import TemplateView
from .models import HomeBanner


class IndexView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['home_banners'] = HomeBanner.objects.all()
        return context
