import datetime
from django.db import models
from django.db.models import Count,  Case, When, BooleanField, TextField, Value as V

from django.db.models.functions import Substr, StrIndex, Cast

from users.models import User


class EventQuerySet(models.QuerySet):

    def get_events_organised_by_user(self, user):
        return self.filter(organiser=user)\
            .annotate(attendees_count=Count('attendees')) \
            .order_by('date_time')

    def get_events_attended_by_user(self, user):
        return self.filter(attendees__in=[user]) \
            .annotate(attendees_count=Count('attendees')) \
            .order_by('date_time')

    def get_current_events(self, _):
        return self.filter(date_time__gte=datetime.datetime.now())\
            .annotate(attendees_count=Count('attendees'))\
            .order_by('date_time')

    def get_events_in_past(self, _):
        return self.filter(date_time__lte=datetime.datetime.now())\
            .annotate(attendees_count=Count('attendees'))\
            .order_by('date_time')

    def get_event(self, pk, user):
        """
        Return a specific event

        :param pk: ID of the Event
        """
        return self.filter(pk=pk)\
            .annotate(is_organiser=Case(When(organiser=user.id, then=V(True)),
                                        default=V(False),
                                        output_field=BooleanField()),
                      is_attending=Case(When(attendees__id=user.id, then=V(True)),
                                        default=V(False),
                                        output_field=BooleanField()),
                      is_in_past=Case(When(date_time__lt=datetime.datetime.now(), then=V(True)),
                                      default=V(False),
                                      output_field=BooleanField()),
                      attendees_count=Count('attendees')).first()


class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(default='')
    organiser = models.ForeignKey(User, related_name='events_organiser', on_delete=models.CASCADE)
    date_time = models.DateTimeField(help_text='Format: YYYY-MM-DD HH:MM:SS')
    attendees = models.ManyToManyField(User, related_name='events_attendees', blank=True)
    objects = EventQuerySet.as_manager()

    def __str__(self):
        return '{0}: {1}'.format(self.date_time, self.title)
