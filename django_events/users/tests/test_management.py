from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth import get_user_model


class TestCreateDefaultSU(TestCase):

    def test_no_super_user_exists(self):
        out = StringIO()
        call_command('create_default_su', stdout=out)
        self.assertIn('Created default superuser', out.getvalue())
        su_count = get_user_model().objects.all().count()
        self.assertEqual(su_count, 1)
        user = get_user_model().objects.filter(email="admin@events.com")
        self.assertTrue(user.exists())

    def test_super_user_exists(self):
        get_user_model().objects.create_superuser(email='Admin1@events.com', password='Password')
        out = StringIO()
        call_command('create_default_su', stdout=out)
        self.assertIn('superuser already exists', out.getvalue())

