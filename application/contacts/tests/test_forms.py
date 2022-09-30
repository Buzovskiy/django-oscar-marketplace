from django.test import TestCase
from django.core import mail
from django.core.validators import validate_email
from django.conf import settings
from application.contacts.forms import ContactsForm
from django.urls import reverse
from django.test.client import RequestFactory
from captcha.models import CaptchaStore


class TestContactsForm(TestCase):
    """
    Testing with simple captcha
    https://stackoverflow.com/questions/3159284/how-to-unit-test-a-form-with-a-captcha-field-in-django
    """

    form_valid_data = {
        'name': 'Ivan',
        'last_name': 'Petrov',
        'email': 'ivan@gmail.com',
        'phone': '+381234567890',
        'country': 'Ukraine',
        'city': 'Odessa',
        'postal_code': 65043,
        'subject': 'subject',
        'message': 'Hello World',
        'shop_question': 'yes',
        'shop_sign': 'example.com',
        'website': 'example.com',
        'accept': True,
        'captcha_0': 'dummy-value',
        'captcha_1': 'PASSED',
    }

    def test_manager(self):
        """
        Тестирование списка email settings.MANAGERS для отправки
        """
        self.assertIsInstance(settings.MANAGERS, list)
        self.assertGreater(len(settings.MANAGERS), 0, msg="Provide email addresses in .env file")
        for name, email in settings.MANAGERS:
            self.assertIsNone(validate_email(email))

    def test_form_validation(self):
        form = ContactsForm(data=self.form_valid_data)
        self.assertTrue(form.is_valid())

    def test_send_email(self):
        form = ContactsForm(data=self.form_valid_data)
        self.assertTrue(form.is_valid())
        request = RequestFactory().get(reverse('contacts:contacts'))
        form.send_email(request)
        self.assertTrue(mail.outbox[0].body)

    def test_become_our_partner_send_email(self):
        form = ContactsForm(data=self.form_valid_data)
        self.assertTrue(form.is_valid())
        request = RequestFactory().get(reverse('contacts:become-our-partner'))
        form.send_email(request)
        self.assertTrue(mail.outbox[0].body)
