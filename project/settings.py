"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import sys
from django.utils.translation import gettext_lazy as _
from oscar.defaults import *

import decouple
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = decouple.config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = decouple.config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = decouple.config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
BASE_URL = decouple.config('BASE_URL')
CLIENT_SITE_NAME = decouple.config('CLIENT_SITE_NAME')
TELEGRAM_BOT_TOKEN = decouple.config('TELEGRAM_BOT_TOKEN')
TELEGRAM_GROUP_CHAT_ID = decouple.config('TELEGRAM_GROUP_CHAT_ID')

DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520  # 20 Mb
DATA_UPLOAD_MAX_NUMBER_FIELDS = 20000

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',

    'oscar.config.Shop',
    'oscar.apps.analytics.apps.AnalyticsConfig',
    'application.checkout.apps.CheckoutConfig',
    'application.address.apps.AddressConfig',
    'application.shipping.apps.ShippingConfig',
    'application.catalogue.apps.CatalogueConfig',
    'oscar.apps.catalogue.reviews.apps.CatalogueReviewsConfig',
    'oscar.apps.communication.apps.CommunicationConfig',
    'application.partner.apps.PartnerConfig',
    'application.basket.apps.BasketConfig',
    'application.payment.apps.PaymentConfig',
    'oscar.apps.offer.apps.OfferConfig',
    'application.order.apps.OrderConfig',
    'application.customer.apps.CustomerConfig',
    'application.search.apps.SearchConfig',

    # 'oscar.apps.voucher.apps.VoucherConfig',
    'oscar.apps.wishlists.apps.WishlistsConfig',
    'oscar.apps.dashboard.apps.DashboardConfig',
    'oscar.apps.dashboard.reports.apps.ReportsDashboardConfig',
    'oscar.apps.dashboard.users.apps.UsersDashboardConfig',
    'oscar.apps.dashboard.orders.apps.OrdersDashboardConfig',
    'oscar.apps.dashboard.catalogue.apps.CatalogueDashboardConfig',
    'oscar.apps.dashboard.offers.apps.OffersDashboardConfig',
    'oscar.apps.dashboard.partners.apps.PartnersDashboardConfig',
    'oscar.apps.dashboard.pages.apps.PagesDashboardConfig',
    'oscar.apps.dashboard.ranges.apps.RangesDashboardConfig',
    'oscar.apps.dashboard.reviews.apps.ReviewsDashboardConfig',
    'oscar.apps.dashboard.vouchers.apps.VouchersDashboardConfig',
    'oscar.apps.dashboard.communications.apps.CommunicationsDashboardConfig',
    'oscar.apps.dashboard.shipping.apps.ShippingDashboardConfig',

    # 3rd-party apps that oscar depends on
    'widget_tweaks',
    'haystack',
    'treebeard',
    'sorl.thumbnail',  # Default thumbnail backend, can be replaced
    'django_tables2',
    'rest_framework',
    'corsheaders',

    'adminsortable2',
    'ckeditor',
    'ckeditor_uploader',
    'rosetta',
    'captcha',
    'testmail',
    'oscar_routing',
    'app_settings',
    'application.blog.apps.BlogConfig',
    'application.contacts.apps.ContactsConfig',
    'application.exchange.apps.ExchangeConfig',
    'application.interview.apps.InterviewConfig',
    'application.search_optimisation_fields.apps.SearchOptimisationFieldsConfig',
    'application.voucher.apps.VoucherConfig'
]

if DEBUG:
    # INSTALLED_APPS += ['debug_toolbar']
    pass

SITE_ID = 1

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'oscar.apps.basket.middleware.BasketMiddleware',
    'application.basket.middleware.APIBasketMiddleware',
    'oscar_routing.middleware.block_ip.BlockedIpMiddleware',
]

if 'debug_toolbar' in INSTALLED_APPS:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.communication.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': decouple.config('DEFAULT_DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': decouple.config('DEFAULT_DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': decouple.config('DEFAULT_DB_USER'),
        'PASSWORD': decouple.config('DEFAULT_DB_PASSWORD'),
        'HOST': decouple.config('DEFAULT_DB_HOST', default='localhost'),
        'PORT': decouple.config('DEFAULT_DB_PORT', default='5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es'

# The language code corresponding to 1c language
LANGUAGE_CODE_1C = 'en'

LANGUAGES = (
    ('es', _('Spanish')),
    ('en', _('English')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    BASE_DIR / 'locale',
)

ROSETTA_MESSAGES_PER_PAGE = 1000
ROSETTA_SHOW_AT_ADMIN_PANEL = True

HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': f"http://solr:{decouple.config('SOLR_PASSWORD')}@127.0.0.1:8983/solr/{decouple.config('SOLR_CORE')}",
        'ADMIN_URL': f"http://solr:{decouple.config('SOLR_PASSWORD')}@127.0.0.1:8983/solr/admin/cores",
        'INCLUDE_SPELLING': True,
    },
}

for lang in LANGUAGES:
    lang_code = lang[0]
    HAYSTACK_CONNECTIONS[lang_code] = {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': f"http://solr:{decouple.config('SOLR_PASSWORD')}@127.0.0.1:8983/solr/{decouple.config('SOLR_CORE')}_{lang_code}",
        'ADMIN_URL': f"http://solr:{decouple.config('SOLR_PASSWORD')}@127.0.0.1:8983/solr/admin/cores",
        'INCLUDE_SPELLING': True,
    }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
# STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [BASE_DIR / 'static_src']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
CKEDITOR_UPLOAD_PATH = "ckeditor-uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 'auto',
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Processed', 'Cancelled',),
    'Cancelled': (),
}

OSCAR_SHOP_NAME = 'Weestep'
OSCAR_SHOP_TAGLINE = 'be bigger'
OSCAR_HOMEPAGE = reverse_lazy('catalogue:index')

OSCAR_PRODUCTS_PER_PAGE = 24

OSCAR_DEFAULT_CURRENCY = 'EUR'

EMAIL_HOST = decouple.config('EMAIL_HOST')
EMAIL_PORT = decouple.config('EMAIL_PORT')
EMAIL_HOST_USER = decouple.config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = decouple.config('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = decouple.config('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_USE_TLS = decouple.config('EMAIL_USE_TLS', default=False, cast=bool)
OSCAR_FROM_EMAIL = decouple.config('OSCAR_FROM_EMAIL')

SERVER_EMAIL = decouple.config('OSCAR_FROM_EMAIL')
EMAIL_SUBJECT_PREFIX = '[POSTMASTER] '

# The Debug Toolbar is shown only if your IP address is listed in the INTERNAL_IPS
INTERNAL_IPS = [
    '127.0.0.1',
]

# Список 2-tuples email адресов, на которые отправляются сообщения со страницы /contacts/
MANAGERS = []
for email in decouple.config('MANAGERS', cast=lambda v: [s.strip() for s in v.split(',')]):
    if email:
        MANAGERS += [('Postmaster', email)]

# Root directory for 1c exchange temporary files
EXCHANGE_ROOT = MEDIA_ROOT / '1c'
# The directory where temporary import and offers xml are stored.
# The string value will be appended to MEDIA_ROOT
EXCHANGE_XML_UPLOAD_TO = '1c/temp/'
# The directory where temporary product images are stored.
# The string value will be appended to MEDIA_ROOT
EXCHANGE_IMAGE_UPLOAD_TO = '1c/temp/images/'

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
# CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_arcs', 'captcha.helpers.noise_dots',)
# CAPTCHA_LETTER_ROTATION = (-1, 1)
CAPTCHA_IMAGE_SIZE = (130, 100)
CAPTCHA_FONT_SIZE = 30
# CAPTCHA_LENGTH = 3
if 'test' in sys.argv:
    CAPTCHA_TEST_MODE = True

# Setting for oscar_routing.middleware.block_ip.BlockedIpMiddleware
BLOCKED_IPS = ['46.161.11.252']

# Attributes code
# that are the result of slugifying when 1c exchanges happen
ATTR_COLOR_CODE = 'tsvet'
ATTR_SIZES_CODE = 'razmery'
# The slug of product class shoes
PRODUCT_CLASS_SHOES_SLUG = 'shoes'
# The partner which is to be added to the database on 1c exchange
PARTNER_DEFAULT = {'code': 'weestep', 'name': 'Weestep'}

# Search facets
OSCAR_SEARCH_FACETS = {
    'fields': OrderedDict([
        # The key for these dicts will be used when passing facet data
        # to the template. Same for the 'queries' dict below.
        # ('product_class', {'name': _('Type'), 'field': 'product_class'}),
        # ('rating', {'name': _('Rating'), 'field': 'rating'}),
        ('category', {'name': _('Type'), 'field': 'category', 'options': {'sort': 'index'}}),
        ('gender', {'name': _('Gender'), 'field': 'gender', 'options': {'sort': 'index'}}),
        ('season', {'name': _('Season'), 'field': 'season', 'options': {'sort': 'index'}}),
        ('size', {'name': _('Size'), 'field': 'size', 'options': {'sort': 'index'}}),
        ('material_verkha', {'name': _('Material outer'), 'field': 'material_verkha', 'options': {'sort': 'index'}}),
        ('material_vnutrennii', {
            'name': _('Material inner'), 'field': 'material_vnutrennii', 'options': {'sort': 'index'}
        }),
        ('color', {'name': _('Color'), 'field': 'color', 'options': {'sort': 'index'}}),
        # You can specify an 'options' element that will be passed to the
        # SearchQuerySet.facet() call.
        # For instance, with Elasticsearch backend, 'options': {'order': 'term'}
        # will sort items in a facet by title instead of number of items.
        # It's hard to get 'missing' to work
        # correctly though as of Solr's hilarious syntax for selecting
        # items without a specific facet:
        # http://wiki.apache.org/solr/SimpleFacetParameters#facet.method
        # 'options': {'missing': 'true'}
    ]),
    'queries': OrderedDict([
        # ('price_range',
        #  {
        #      'name': _('Price range'),
        #      'field': 'price',
        #      'queries': [
        #          # This is a list of (name, query) tuples where the name will
        #          # be displayed on the front-end.
        #          (_('0 to 20'), '[0 TO 20]'),
        #          (_('20 to 40'), '[20 TO 40]'),
        #          (_('40 to 60'), '[40 TO 60]'),
        #          (_('60+'), '[60 TO *]'),
        #      ]
        #  }),
    ]),
}

OSCAR_REQUIRED_ADDRESS_FIELDS = ('first_name', 'last_name', 'phone_number', 'line1', 'postcode')

LOGIN_REDIRECT_URL = reverse_lazy('catalogue:index')

OSCAR_ALLOW_ANON_CHECKOUT = True

OSCAR_BASKET_COOKIE_SECURE = True

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
