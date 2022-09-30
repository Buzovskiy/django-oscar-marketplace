from oscar.core.application import OscarConfig
from django.urls import path
from oscar.core.loading import get_class


class ContactsConfig(OscarConfig):
    contacts_view = become_our_partner = None
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'contacts'
    name = 'application.contacts'
    namespace = 'contacts'

    def ready(self):
        self.contacts_view = get_class('contacts.views', 'ContactsView')
        self.become_our_partner = get_class('contacts.views', 'BecomeOurPartnerView')

    def get_urls(self):
        urls = [
            path('', self.contacts_view.as_view(), name='contacts'),
            path('become-our-partner', self.become_our_partner.as_view(), name='become-our-partner'),
        ]
        return self.post_process_urls(urls)
