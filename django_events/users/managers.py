from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _lazy


class UserManager(BaseUserManager):

    def create_user(self, email, password, **other_fields):
        """
        Creates a standard user

        :param email: Email Address (username)
        :type email: str
        :param password: Password
        :type password: str
        :param other_fields: Any other fields
        :type other_fields: dict

        :return: The user created
        """
        if not email:
            raise ValueError(_lazy('Missing Email Address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        """
        Creates a super user

        :param email: Email Address (username)
        :type email: str
        :param password: Password
        :type password: str
        :param other_fields: Any other fields
        :type other_fields: dict

        :return: The user created
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        return self.create_user(email, password, **other_fields)
