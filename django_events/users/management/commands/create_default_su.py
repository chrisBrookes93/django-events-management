from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Creates a default super user if one doesn't already exist. " \
           "This is designed to be used in the docker-compose.yml to create an initial super user on deployment."

    def handle(self, *args, **kwargs):
        """
        Checks whether any super users exist and creates a default one if not

        :param args: Unused
        :param kwargs: Unused
        """
        super_users = get_user_model().objects.filter(is_superuser=True)

        if super_users.exists():
            self.stdout.write('A superuser already exists, not creating one')
        else:
            get_user_model().objects.create_superuser(email="admin@events.com", password="EventsEvents")
            self.stdout.write('Created default superuser "admin@events.com"')
            self.stdout.write('Make sure you change the password immediately!')
