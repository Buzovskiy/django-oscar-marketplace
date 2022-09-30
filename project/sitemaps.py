from django.contrib import sitemaps
from django.urls import reverse
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from datetime import datetime
from oscar.core.loading import get_model


class HomeViewSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = 'monthly'
    lastmod = datetime.now()
    protocol = 'https'

    def items(self):
        return ['']

    def location(self, item):
        return item


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    lastmod = datetime.now()
    protocol = 'https'

    def items(self):
        return [
            {'label': 'partner:stores', 'kwargs': {}},
            {'label': 'django.contrib.flatpages.views.flatpage', 'kwargs': {'url': 'about-us/'}},
            {'label': 'django.contrib.flatpages.views.flatpage', 'kwargs': {'url': 'brand-of-the-year/'}},
            {'label': 'django.contrib.flatpages.views.flatpage', 'kwargs': {'url': 'size-guide/'}},
            {'label': 'catalogue:index', 'kwargs': {}},
            {'label': 'contacts:become-our-partner', 'kwargs': {}},
            {'label': 'contacts:contacts', 'kwargs': {}},
        ]

    def location(self, item):
        return reverse(item['label'], kwargs=item['kwargs'])


class ProductSitemap(sitemaps.Sitemap):
    changefreq = "monthly"
    priority = 0.7
    protocol = 'https'

    def items(self):
        product = get_model('catalogue', 'Product')
        return product.objects.browsable()

    def lastmod(self, obj):
        return obj.date_updated


sitemaps = {
    'home': HomeViewSitemap,
    'static': StaticViewSitemap,
    'product': ProductSitemap,
}

sitemap_url_patterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]
