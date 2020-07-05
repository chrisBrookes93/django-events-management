from datetime import datetime, timedelta
from django.test import TestCase, RequestFactory
from django.shortcuts import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from events.views import EventCreate, EventUpdate, EventList, UnattendEvent, AttendEvent, EventView
from events.models import Event

HTTP_OK = 200
HTTP_REDIRECT = 302
HTTP_NOT_FOUND = 404
HTTP_FORBIDDEN = 403


class TestEventCreate(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.request_factory = RequestFactory()
        cls.user1 = get_user_model().objects.create_user(email='user1@events.com', password='password')

    def test_event_create_not_authenticated(self):
        request = self.request_factory.post(reverse('events_create'))
        request.user = AnonymousUser()
        response = EventCreate.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertIn(reverse('user_login'), response.url)

    def test_event_create_invalid_form(self):
        request = self.request_factory.post(reverse('events_create'))
        request.user = self.user1
        response = EventCreate.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertTrue(response.context_data['form'].errors)

    def test_event_create_not_post(self):
        request = self.request_factory.get(reverse('events_create'))
        request.user = self.user1
        response = EventCreate.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)

    def test_event_create_valid_form(self):
        request = self.request_factory.post(reverse('events_create'), data={'title': 'event 1',
                                                                            'description': 'event one',
                                                                            'date_time': '2020-06-26 01:01:12'})
        request.user = self.user1
        response = EventCreate.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertRegexpMatches(response.url, '/events/[\\d]+')


class TestEventUpdate(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.request_factory = RequestFactory()
        cls.user1 = get_user_model().objects.create_user(email='user1@events.com', password='password')
        cls.user2 = get_user_model().objects.create_user(email='user2@events.com', password='password')
        cls.event1 = Event.objects.create(title='Event 1',
                                          description='Event Desc. 1',
                                          date_time=datetime.now(),
                                          organiser=cls.user1)

    def test_event_update_not_authenticated(self):
        request = self.request_factory.post(reverse('events_edit', kwargs={'pk': self.event1.id}))
        request.user = AnonymousUser()
        response = EventUpdate.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_FORBIDDEN)

    def test_event_update_not_permitted(self):
        request = self.request_factory.post(reverse('events_edit', kwargs={'pk': self.event1.id}))
        request.user = self.user2
        response = EventUpdate.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_FORBIDDEN)

    def test_event_update_invalid_event(self):
        request = self.request_factory.post(reverse('events_edit', kwargs={'pk': 99999}))
        request.user = self.user2
        response = EventUpdate.as_view()(request, *[], **{'pk': 99999})
        self.assertEqual(response.status_code, HTTP_FORBIDDEN)

    def test_event_update_not_post(self):
        request = self.request_factory.get(reverse('events_edit', kwargs={'pk': self.event1.id}))
        request.user = self.user1
        response = EventUpdate.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_OK)

    def test_event_update_valid_form(self):
        request = self.request_factory.post(
            reverse('events_edit', kwargs={'pk': self.event1.id}),
            data={'title': '#event 1',
                  'description': '#event one',
                  'date_time': '2020-06-26 01:01:12'})
        request.user = self.user1
        response = EventUpdate.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertRegexpMatches(response.url, reverse('events_view', args=(self.event1.id,)))


class TestViewEventAttend(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.request_factory = RequestFactory()
        cls.user1 = get_user_model().objects.create_user(email='user1@events.com', password='password')
        cls.user2 = get_user_model().objects.create_user(email='user2@events.com', password='password')
        cls.event1 = Event.objects.create(title='Event 1',
                                          description='Event Desc. 1',
                                          date_time=datetime.now(),
                                          organiser=cls.user1)

    def test_view_event_attend_not_authenticated(self):
        request = self.request_factory.post(reverse('events_attend', kwargs={'pk': self.event1.id}))
        request.user = AnonymousUser()
        response = AttendEvent.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertIn('login', response.url)

    def test_view_event_attend_invalid_event(self):
        request = self.request_factory.post(reverse('events_attend', kwargs={'pk': 9999}))
        request.user = self.user1
        response = AttendEvent.as_view()(request, *[], **{'pk': 9999})
        self.assertEqual(response.status_code, HTTP_NOT_FOUND)

    def test_view_event_attend_correct_case(self):
        request = self.request_factory.post(reverse('events_attend', kwargs={'pk': self.event1.id}))
        request.user = self.user1
        response = AttendEvent.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertEqual(reverse('events_view', args=(self.event1.id,)), response.url)


class TestViewEventUnattend(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.request_factory = RequestFactory()
        cls.user1 = get_user_model().objects.create_user(email='user1@events.com', password='password')
        cls.user2 = get_user_model().objects.create_user(email='user2@events.com', password='password')
        cls.event1 = Event.objects.create(title='Event 1',
                                          description='Event Desc. 1',
                                          date_time=datetime.now(),
                                          organiser=cls.user1)
        cls.event1.attendees.add(cls.user1)
        cls.event1.save()

    def test_view_event_unattend_not_authenticated(self):
        request = self.request_factory.post(reverse('events_unattend', kwargs={'pk': self.event1.id}))
        request.user = AnonymousUser()
        response = UnattendEvent.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertIn('login', response.url)

    def test_view_event_unattend_invalid_event(self):
        request = self.request_factory.post(reverse('events_unattend', kwargs={'pk': 9999}))
        request.user = self.user1
        response = UnattendEvent.as_view()(request, *[], **{'pk': 9999})
        self.assertEqual(response.status_code, HTTP_NOT_FOUND)

    def test_view_event_unattend_correct_case(self):
        request = self.request_factory.post(reverse('events_unattend', kwargs={'pk': self.event1.id}))
        request.user = self.user1
        response = UnattendEvent.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertEqual(reverse('events_view', args=(self.event1.id,)), response.url)


class TestViewEventView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.request_factory = RequestFactory()
        cls.user1 = get_user_model().objects.create_user(email='user1@events.com', password='password')
        cls.user2 = get_user_model().objects.create_user(email='user2@events.com', password='password')
        cls.event1 = Event.objects.create(title='Event 1',
                                          description='Event Desc. 1',
                                          date_time=datetime.now(),
                                          organiser=cls.user1)
        cls.event1.attendees.add(cls.user1)
        cls.event1.save()

    def test_view_event_view_not_authenticated(self):
        request = self.request_factory.get(reverse('events_view', kwargs={'pk': self.event1.id}))
        request.user = AnonymousUser()
        response = EventView.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertIn('login', response.url)

    def test_view_event_view_invalid_event(self):
        request = self.request_factory.get(reverse('events_view', kwargs={'pk': 9999}))
        request.user = self.user1
        response = EventView.as_view()(request, *[], **{'pk': 9999})
        self.assertEqual(response.status_code, HTTP_NOT_FOUND)

    def test_view_event_view_correct_case(self):
        request = self.request_factory.get(reverse('events_view', kwargs={'pk': self.event1.id}))
        request.user = self.user1
        response = EventView.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertInHTML(self.event1.description, response.content.decode())


class TestViewEventList(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.request_factory = RequestFactory()
        cls.user1 = get_user_model().objects.create_user(email='user1@events.com', password='password')
        cls.user2 = get_user_model().objects.create_user(email='user2@events.com', password='password')
        cls.organised_event = Event.objects.create(title='Organised Event 1',
                                                   description='Event Desc. 1',
                                                   date_time=datetime.now() + timedelta(hours=2),
                                                   organiser=cls.user1)

        cls.organised_event.attendees.add(cls.user2)
        cls.organised_event.save()

        cls.attending_event = Event.objects.create(title='Attending Event 1',
                                                   description='Event Desc. 1',
                                                   date_time=datetime.now() + timedelta(hours=2),
                                                   organiser=cls.user2)
        cls.attending_event.attendees.add(cls.user1)
        cls.attending_event.save()

        cls.expired_event = Event.objects.create(title='Passed Event 1',
                                                 description='Event Desc. 1',
                                                 date_time=datetime.now() - timedelta(hours=4),
                                                 organiser=cls.user1)

    def test_view_event_list_not_authenticated(self):
        request = self.request_factory.get(reverse('events_list'))
        request.user = AnonymousUser()
        response = EventList.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertIn('login', response.url)

    def test_view_event_list_all(self):
        request = self.request_factory.get(reverse('events_list'))
        request.user = self.user1
        response = EventList.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertInHTML(self.organised_event.title, response.content.decode())
        self.assertInHTML(self.attending_event.title, response.content.decode())

    def test_view_event_list_organised(self):
        request = self.request_factory.get(reverse('events_list'), data={'filter': 'o'})
        request.user = self.user1
        response = EventList.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertInHTML(self.organised_event.title, response.content.decode())

    def test_view_event_list_attending(self):
        request = self.request_factory.get(reverse('events_list'), data={'filter': 'a'})
        request.user = self.user1
        response = EventList.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertInHTML(self.attending_event.title, response.content.decode())

    def test_view_event_list_past(self):
        request = self.request_factory.get(reverse('events_list'), data={'filter': 'p'})
        request.user = self.user1
        response = EventList.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertInHTML(self.expired_event.title, response.content.decode())

    def test_view_event_list_page_not_int(self):
        request = self.request_factory.get(reverse('events_list'), data={'page': 'pageOne', 'filter': 'a'})
        request.user = self.user1
        response = EventList.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertInHTML(self.attending_event.title, response.content.decode())

    def test_view_event_list_page_empty(self):
        request = self.request_factory.get(reverse('events_list'), data={'page': 999, 'filter': 'a'})
        request.user = self.user1
        response = EventList.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertInHTML(self.attending_event.title, response.content.decode())
