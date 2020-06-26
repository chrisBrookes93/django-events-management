from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from ..views import view_index


class TestViewIndex(TestCase):

    HTTP_REDIRECT = 302
    HTTP_OK = 200

    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(email='user1@events.com', password='password')
        cls.request_factory = RequestFactory()

    def test__view_index__authenticated(self):
        request = self.request_factory.get(reverse('index'))
        request.user = self.user1
        response = view_index(request)
        self.assertEqual(response.status_code, TestViewIndex.HTTP_REDIRECT)
        self.assertEqual(response.url, '/events/')

    def test__view_index__not_authenticated(self):
        request = self.request_factory.get(reverse('index'))
        request.user = AnonymousUser()
        response = view_index(request)
        self.assertEqual(response.status_code, TestViewIndex.HTTP_OK)
        self.assertInHTML('Welcome to Event-ing', response.content.decode())