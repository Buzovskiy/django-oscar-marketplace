from django.conf import settings
from oscar.apps.customer.views import AccountAuthView as CoreAccountAuthView


class AccountAuthView(CoreAccountAuthView):
    def get_login_success_url(self, form):
        redirect_url = form.cleaned_data['redirect_url']
        if redirect_url:
            return redirect_url

        return settings.LOGIN_REDIRECT_URL
