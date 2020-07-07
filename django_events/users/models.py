from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
import re

from .managers import UserManager

EMAIL_FRIENDLY_REGEX = re.compile('(.*)@')


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email Address', unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    @classmethod
    def from_db(cls, db, field_names, values):
        """
        Override to set a friendly name attribute on the instance. This is the first part of the email address (before
        the '@')
        """
        instance = super(AbstractBaseUser, cls).from_db(db, field_names, values)
        matches = re.search(EMAIL_FRIENDLY_REGEX, instance.email)
        instance.friendly_name = matches.group(1) if matches else instance.email
        return instance
