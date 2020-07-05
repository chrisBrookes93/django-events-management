from django.test import TestCase, RequestFactory
from django.urls import reverse

from users.views import RegisterView


class TestViewRegister(TestCase):

    HTTP_REDIRECT = 302
    HTTP_OK = 200

    @classmethod
    def setUpTestData(cls):
        cls.request_factory = RequestFactory()

    def test_register_view_not_post(self):
        request = self.request_factory.get(reverse('user_register'))
        response = RegisterView.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, TestViewRegister.HTTP_OK)
        self.assertInHTML('<title>Register</title>', response.content.decode())

    def test_register_view_invalid_form(self):
        request = self.request_factory.post(reverse('user_register'))
        response = RegisterView.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, TestViewRegister.HTTP_OK)
        self.assertInHTML('<title>Register</title>', response.content.decode())

    def test_register_view_valid_form(self):

        request = self.request_factory.post(reverse('user_register'), data={'email': 'user1@events.com',
                                                                            'password1': 'Events246810',
                                                                            'password2': 'Events246810'})
        request.session = self.client.session
        response = RegisterView.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, TestViewRegister.HTTP_REDIRECT)
        self.assertEqual(response.url, reverse('events_list'))
