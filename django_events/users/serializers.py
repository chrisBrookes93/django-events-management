from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    # Not part of the User model but added as an attribute in User.from_db() for convenience
    friendly_name = serializers.CharField(read_only=True, default='')

    class Meta:
        model = get_user_model()
        fields = ['email', 'friendly_name']
