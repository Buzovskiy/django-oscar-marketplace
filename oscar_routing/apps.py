from oscar import config
from django.urls import path, reverse_lazy, include
from django.apps import apps


class OscarRoutingConfig(config.Shop):
    home_app = partner_app = blog_app = flatpages_app = contacts_app = exchange_app = interview_app = None

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'oscar_routing'

    def ready(self):
        super().ready()
        self.home_app = apps.get_app_config('home')
        self.partner_app = apps.get_app_config('partner')
        self.blog_app = apps.get_app_config('blog')
        self.flatpages_app = include('django.contrib.flatpages.urls')
        self.contacts_app = apps.get_app_config('contacts')
        self.exchange_app = apps.get_app_config('exchange')
        self.interview_app = apps.get_app_config('interview')

    def get_urls(self):
        from django.contrib.auth import views as auth_views

        from oscar.views.decorators import login_forbidden

        urls = [
            path('', self.home_app.urls),  # home page link
            path('', self.partner_app.urls),  # stores page
            path('', self.blog_app.urls),
            path('interview/', self.interview_app.urls),
            path('1c_exchange/', self.exchange_app.urls),
            path('contacts/', self.contacts_app.urls),
            path('pages/', self.flatpages_app),
            path('catalogue/', self.catalogue_app.urls),
            path('basket/', self.basket_app.urls),
            path('checkout/', self.checkout_app.urls),
            path('accounts/', self.customer_app.urls),
            path('search/', self.search_app.urls),
            path('dashboard/', self.dashboard_app.urls),
            path('offers/', self.offer_app.urls),

            # Password reset - as we're using Django's default view functions,
            # we can't namespace these urls as that prevents
            # the reverse function from working.
            path('password-reset/',
                 login_forbidden(
                     auth_views.PasswordResetView.as_view(
                         form_class=self.password_reset_form,
                         success_url=reverse_lazy('password-reset-done'),
                         template_name='oscar/registration/password_reset_form.html'
                     )
                 ),
                 name='password-reset'),
            path('password-reset/done/',
                 login_forbidden(auth_views.PasswordResetDoneView.as_view(
                     template_name='oscar/registration/password_reset_done.html'
                 )),
                 name='password-reset-done'),
            path('password-reset/confirm/<str:uidb64>/<str:token>/',
                 login_forbidden(
                     auth_views.PasswordResetConfirmView.as_view(
                         form_class=self.set_password_form,
                         success_url=reverse_lazy('password-reset-complete'),
                         template_name='oscar/registration/password_reset_confirm.html'
                     )
                 ),
                 name='password-reset-confirm'),
            path('password-reset/complete/',
                 login_forbidden(auth_views.PasswordResetCompleteView.as_view(
                     template_name='oscar/registration/password_reset_complete.html'
                 )),
                 name='password-reset-complete'),
        ]
        return urls
