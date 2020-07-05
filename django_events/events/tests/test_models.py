from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

from events.models import Event


class TestEventQuerySet(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(email='user1@events.com', password='Password')
        cls.user2 = get_user_model().objects.create_user(email='user2@events.com', password='Password')
        cls.user3 = get_user_model().objects.create_user(email='user3@events.com', password='Password')

        cls.past_event1 = Event.objects.create(title='Past Event 1',
                                               description='Past Event Desc. 1',
                                               date_time=datetime.now() - timedelta(hours=4),
                                               organiser=cls.user1)

        cls.past_event2 = Event.objects.create(title='Past Event 2',
                                               description='Past Event Desc. 2',
                                               date_time=datetime.now() - timedelta(hours=2),
                                               organiser=cls.user2)
        cls.past_event2.attendees.add(cls.user3)
        cls.past_event2.attendees.add(cls.user2)
        cls.past_event2.save()

        cls.future_event1 = Event.objects.create(title='Future Event 1',
                                                 description='Event Desc. 1',
                                                 date_time=datetime.now() + timedelta(hours=2),
                                                 organiser=cls.user1)
        cls.future_event1.attendees.add(cls.user2)
        cls.future_event1.attendees.add(cls.user1)
        cls.future_event1.save()

        cls.future_event2 = Event.objects.create(title='Future Event 2',
                                                 description='Future Event Desc. 2',
                                                 date_time=datetime.now() + timedelta(hours=4),
                                                 organiser=cls.user2)

    def test_get_current_events_all_dates_in_future(self):
        events = Event.objects.get_current_events()
        self.assertIn(self.future_event1, events)
        self.assertIn(self.future_event2, events)
        self.assertNotIn(self.past_event1, events)
        self.assertNotIn(self.past_event2, events)

    def test_get_current_events_correct_organiser_name(self):
        events = Event.objects.get_current_events()
        event = events.get(pk=self.future_event1.id)
        self.assertEqual(event.organiser.friendly_name, 'user1')

    def test_get_current_events_correct_attendee_count(self):
        events = Event.objects.get_current_events()
        event = events.get(pk=self.future_event1.id)
        self.assertEqual(event.attendees_count, 2)

    def test_get_current_events_correct_ordering(self):
        events = Event.objects.get_current_events()
        first_event_dt = events[0].date_time
        second_event_dt = events[1].date_time
        self.assertTrue(first_event_dt < second_event_dt)

    def test_get_events_in_past_all_dates_in_past(self):
        events = Event.objects.get_events_in_past()
        self.assertIn(self.past_event1, events)
        self.assertIn(self.past_event2, events)
        self.assertNotIn(self.future_event1, events)
        self.assertNotIn(self.future_event2, events)

    def test_get_events_in_past_correct_organiser_name(self):
        events = Event.objects.get_events_in_past()
        event = events.get(pk=self.past_event1.id)
        self.assertEqual(event.organiser.friendly_name, 'user1')

    def test_get_events_in_past_correct_attendee_count(self):
        events = Event.objects.get_events_in_past()
        event = events.get(pk=self.past_event2.id)
        self.assertEqual(event.attendees_count, 2)

    def test_get_events_in_past_correct_ordering(self):
        events = Event.objects.get_events_in_past()
        first_event_dt = events[0].date_time
        second_event_dt = events[1].date_time
        self.assertTrue(first_event_dt < second_event_dt)

    def test_get_events_attended_by_user_correct_events(self):
        events = Event.objects.get_events_attended_by_user(self.user2)
        self.assertIn(self.past_event2, events)
        self.assertIn(self.future_event1, events)
        self.assertNotIn(self.past_event1, events)
        self.assertNotIn(self.future_event2, events)

    def test_get_events_attended_by_user_correct_organiser_name(self):
        events = Event.objects.get_events_attended_by_user(self.user2)
        event = events.get(pk=self.past_event2.id)
        self.assertEqual(event.organiser.friendly_name, 'user2')

    def test_get_events_attended_by_user_correct_attendee_count(self):
        events = Event.objects.get_events_attended_by_user(self.user2)
        event = events.get(pk=self.future_event1.id)
        self.assertEqual(event.attendees_count, 1)

    def test_get_events_attended_by_user_correct_ordering(self):
        events = Event.objects.get_events_attended_by_user(self.user2)
        first_event_dt = events[0].date_time
        second_event_dt = events[1].date_time
        self.assertTrue(first_event_dt < second_event_dt)

    def test_get_events_organised_by_user_correct_events(self):
        events = Event.objects.get_events_organised_by_user(self.user1)
        self.assertIn(self.past_event1, events)
        self.assertIn(self.future_event1, events)
        self.assertNotIn(self.past_event2, events)
        self.assertNotIn(self.future_event2, events)

    def test_get_events_organised_by_user_correct_organiser_name(self):
        events = Event.objects.get_events_organised_by_user(self.user1)
        event = events.get(pk=self.past_event1.id)
        self.assertEqual(event.organiser.friendly_name, 'user1')

    def test_get_events_organised_by_user_correct_attendee_count(self):
        events = Event.objects.get_events_organised_by_user(self.user1)
        event = events.get(pk=self.future_event1.id)
        self.assertEqual(event.attendees_count, 2)

    def test_get_events_organised_by_user_correct_ordering(self):
        events = Event.objects.get_events_organised_by_user(self.user1)
        first_event_dt = events[0].date_time
        second_event_dt = events[1].date_time
        self.assertTrue(first_event_dt < second_event_dt)

    def test_get_event_correct_event(self):
        event = Event.objects.get_event(self.future_event1.id, self.user1)
        self.assertEqual(event, self.future_event1)
