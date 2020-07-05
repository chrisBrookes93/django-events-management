from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Event, EventQuerySet


class BaseEventSerializer(serializers.ModelSerializer):
    organiser = serializers.ReadOnlyField(source='organiser.email')
    organiser_friendly_name = serializers.CharField(source='organiser.friendly_name', read_only=True)

    class Meta:
        model = Event
        fields = ['title', 'description', 'date_time', 'organiser_friendly_name', 'organiser', 'url']


class EventListSerializer(BaseEventSerializer):
    attendees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ['title', 'description', 'date_time', 'attendees_count', 'organiser_friendly_name', 'organiser', 'url']


class EventDetailSerializer(EventListSerializer):
    attendees = UserSerializer(many=True, read_only=True)
    # These fields are not part of the model but are annotations added by EvenyQuerySet.get_event()
    is_organiser = serializers.BooleanField(read_only=True)
    is_in_past = serializers.BooleanField(read_only=True)
    is_attending = serializers.BooleanField(read_only=True)

    class Meta:
        model = Event
        fields = ['title', 'description', 'date_time', 'organiser_friendly_name', 'organiser', 'attendees',
                  'is_organiser', 'is_in_past', 'is_attending']
