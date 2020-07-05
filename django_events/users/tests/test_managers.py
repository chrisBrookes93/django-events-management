from django.test import TestCase
from users.models import User


class TestUserManager(TestCase):

    def test_create_user_correct(self):
        user = User.objects.create_user(email='user1@events.com', password='Password')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser_correct(self):
        user = User.objects.create_superuser(email='user1@events.com', password='Password')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
