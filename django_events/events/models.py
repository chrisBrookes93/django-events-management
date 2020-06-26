import datetime
from django.db import models
from django.db.models import Value as V
from django.db.models import TextField
from django.db.models import Count
from django.db.models.functions import Substr, StrIndex, Cast

from users.models import User


class EventQuerySet(models.QuerySet):

    def get_events_organised_by_user(self, user):
        return \
            self.filter(organiser=user)\
                .annotate(attendees_count=Count('attendees'),
                          organiser_friendly=Cast(
                              Substr('organiser__email',
                                     1,
                                     StrIndex(
                                         "organiser__email",
                                         (V("@"))) - 1),
                              TextField())) \
                .order_by('date_time')

    def get_events_attended_by_user(self, user):
        return \
            self.filter(attendees__in=[user]) \
                .annotate(attendees_count=Count('attendees'),
                          organiser_friendly=Cast(
                              Substr('organiser__email',
                                     1,
                                     StrIndex(
                                         "organiser__email",
                                         (V("@"))) - 1),
                              TextField())) \
                .order_by('date_time')

    def get_current_events(self):
        return \
            self.filter(date_time__gte=datetime.datetime.now())\
                .annotate(attendees_count=Count('attendees'),
                          organiser_friendly=Cast(
                              Substr('organiser__email',
                                     1,
                                     StrIndex(
                                         "organiser__email",
                                         (V("@"))) - 1),
                              TextField())) \
                .order_by('date_time')

    def get_events_in_past(self):
        return \
            self.filter(date_time__lte=datetime.datetime.now())\
                .annotate(attendees_count=Count('attendees'),
                          organiser_friendly=Cast(
                              Substr('organiser__email',
                                     1,
                                     StrIndex(
                                         "organiser__email",
                                         (V("@"))) - 1),
                              TextField())) \
                .order_by('date_time')

    def get_event(self, event_id):
        """
        Return a specific event

        :param event_id: ID of the Event
        """
        return self.get(pk=event_id)


class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(default='')
    organiser = models.ForeignKey(User, related_name='events_organiser', on_delete=models.CASCADE)
    date_time = models.DateTimeField(help_text='Format: YYYY-MM-DD HH:MM:SS')
    attendees = models.ManyToManyField(User, related_name='events_attendees', blank=True)
    objects = EventQuerySet.as_manager()

    def __str__(self):
        return '{0}: {1} (organised by: {2})'.format(self.date_time, self.title, self.organiser)
