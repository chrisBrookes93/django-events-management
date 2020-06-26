from django.test import TestCase, RequestFactory
from django.urls import reverse

from ..views import view_register


class TestViewRegister(TestCase):

    HTTP_REDIRECT = 302
    HTTP_OK = 200

    @classmethod
    def setUpTestData(cls):
        cls.request_factory = RequestFactory()

    def test__register_view__not_post(self):
        request = self.request_factory.get(reverse('user_register'))
        response = view_register(request)
        self.assertEqual(response.status_code, TestViewRegister.HTTP_OK)
        self.assertInHTML('<title>Register</title>', response.content.decode())

    def test__register_view__invalid_form(self):
        request = self.request_factory.post(reverse('user_register'))
        response = view_register(request)
        self.assertEqual(response.status_code, TestViewRegister.HTTP_OK)
        self.assertInHTML('<title>Register</title>', response.content.decode())

    def test__register_view__valid_form(self):

        request = self.request_factory.post(reverse('user_register'), data={'email': 'user1@events.com',
                                                                            'password1': 'Events246810',
                                                                            'password2': 'Events246810'})
        request.session = self.client.session
        response = view_register(request)
        self.assertEqual(response.status_code, TestViewRegister.HTTP_REDIRECT)
        self.assertEqual(response.url, '/')
