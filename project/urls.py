"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.apps import apps
from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _
from .sitemaps import sitemap_url_patterns

urlpatterns = [
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('i18n/', include('django.conf.urls.i18n')),

    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.

    # path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('testmail/', include('testmail.urls')),
    path('1c_exchange/', include(apps.get_app_config('exchange').urls[0])),
    path('v1/checkout/', include('application.checkout.webhook_urls')),
    # path('', include(apps.get_app_config('oscar').urls[0])),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include(apps.get_app_config('oscar_routing').urls[0])),
    path('v1/basket/', include('application.basket.urls')),
    path('v1/checkout/', include('application.checkout.urls')),
    prefix_default_language=True
)

urlpatterns += sitemap_url_patterns

urlpatterns += [url(r'^ckeditor/', include('ckeditor_uploader.urls'))]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += i18n_patterns(
        re_path(r'^rosetta/', include('rosetta.urls')),
        prefix_default_language=False
    )

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.index_title = _('Administration panel')
admin.site.site_header = settings.OSCAR_SHOP_NAME + ' - ' + settings.OSCAR_SHOP_TAGLINE + '. ' \
                         + _('Brand site administration panel')
admin.site.site_title = settings.OSCAR_SHOP_NAME + ' - ' + settings.OSCAR_SHOP_TAGLINE
