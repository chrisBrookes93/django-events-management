from datetime import datetime, timedelta
from django.test import TestCase, RequestFactory
from django.shortcuts import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

from ..views import EventCreate, EventUpdate, view_event_attend, view_event_list, view_event_view, view_event_unattend
from ..models import Event

HTTP_OK = 200
HTTP_REDIRECT = 302


class TestEventCreate(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.request_factory = RequestFactory()
        cls.user1 = get_user_model().objects.create_user(email='user1@events.com', password='password')

    def test__event_create__not_authenticated(self):
        request = self.request_factory.post(reverse('events_create'))
        request.user = AnonymousUser()
        response = EventCreate.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertIn('login', response.url)

    def test__event_create__invalid_form(self):
        request = self.request_factory.post(reverse('events_create'))
        request.user = self.user1
        response = EventCreate.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertTrue(response.context_data['form'].errors)

    def test__event_create__not_post(self):
        request = self.request_factory.get(reverse('events_create'))
        request.user = self.user1
        response = EventCreate.as_view()(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)

    def test__event_create__valid_form(self):
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

    def test__event_update__not_authenticated(self):
        request = self.request_factory.post(reverse('events_edit', kwargs={'pk': self.event1.id}))
        request.user = AnonymousUser()
        response = EventUpdate.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        expected_url = '/events/' + str(self.event1.id)
        self.assertEqual(expected_url, response.url)

    def test__event_update__not_permitted(self):
        request = self.request_factory.post(reverse('events_edit', kwargs={'pk': self.event1.id}))
        request.user = self.user2
        response = EventUpdate.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        expected_url = '/events/' + str(self.event1.id)
        self.assertEqual(expected_url, response.url)

    def test__event_update__invalid_event(self):
        request = self.request_factory.post(reverse('events_edit', kwargs={'pk': 99999}))
        request.user = self.user2
        response = EventUpdate.as_view()(request, *[], **{'pk': 99999})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        expected_url = '/events/' + str(99999)
        self.assertEqual(expected_url, response.url)

    def test__event_update__not_post(self):
        request = self.request_factory.get(reverse('events_edit', kwargs={'pk': self.event1.id}))
        request.user = self.user1
        response = EventUpdate.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_OK)

    def test__event_update__valid_form(self):
        request = self.request_factory.post(
            reverse('events_edit', kwargs={'pk': self.event1.id}),
            data={'title': '#event 1',
                  'description': '#event one',
                  'date_time': '2020-06-26 01:01:12'})
        request.user = self.user1
        response = EventUpdate.as_view()(request, *[], **{'pk': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertRegexpMatches(response.url, '/events/[\\d]+')


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

    def test__view_event_attend__not_authenticated(self):
        request = self.request_factory.post(reverse('events_attend', kwargs={'event_id': self.event1.id}))
        request.user = AnonymousUser()
        response = view_event_attend(request, *[], **{'event_id': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertIn('login', response.url)

    def test__view_event_attend__invalid_event(self):
        request = self.request_factory.post(reverse('events_attend', kwargs={'event_id': 9999}))
        request.user = self.user1
        response = view_event_attend(request, *[], **{'event_id': 9999})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertEqual('/events/', response.url)

    def test__view_event_attend__correct_case(self):
        request = self.request_factory.post(reverse('events_attend', kwargs={'event_id': self.event1.id}))
        request.user = self.user1
        response = view_event_attend(request, *[], **{'event_id': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertEqual('/events/' + str(self.event1.id), response.url)


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

    def test__view_event_unattend__not_authenticated(self):
        request = self.request_factory.post(reverse('events_unattend', kwargs={'event_id': self.event1.id}))
        request.user = AnonymousUser()
        response = view_event_unattend(request, *[], **{'event_id': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertIn('login', response.url)

    def test__view_event_unattend__invalid_event(self):
        request = self.request_factory.post(reverse('events_unattend', kwargs={'event_id': 9999}))
        request.user = self.user1
        response = view_event_unattend(request, *[], **{'event_id': 9999})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertEqual('/events/', response.url)

    def test__view_event_unattend__correct_case(self):
        request = self.request_factory.post(reverse('events_unattend', kwargs={'event_id': self.event1.id}))
        request.user = self.user1
        response = view_event_unattend(request, *[], **{'event_id': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertEqual('/events/' + str(self.event1.id), response.url)


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

    def test__view_event_view__not_authenticated(self):
        request = self.request_factory.post(reverse('events_view', kwargs={'event_id': self.event1.id}))
        request.user = AnonymousUser()
        response = view_event_view(request, *[], **{'event_id': self.event1.id})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertIn('login', response.url)

    def test__view_event_view__invalid_event(self):
        request = self.request_factory.post(reverse('events_view', kwargs={'event_id': 9999}))
        request.user = self.user1
        response = view_event_view(request, *[], **{'event_id': 9999})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertEqual('/events/', response.url)

    def test__view_event_view__correct_case(self):
        request = self.request_factory.post(reverse('events_view', kwargs={'event_id': self.event1.id}))
        request.user = self.user1
        response = view_event_view(request, *[], **{'event_id': self.event1.id})
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

    def test__view_event_list__not_authenticated(self):
        request = self.request_factory.get(reverse('events_list'))
        request.user = AnonymousUser()
        response = view_event_list(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_REDIRECT)
        self.assertIn('login', response.url)

    def test__view_event_list__all(self):
        request = self.request_factory.get(reverse('events_list'))
        request.user = self.user1
        response = view_event_list(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertInHTML(self.organised_event.title, response.content.decode())
        self.assertInHTML(self.attending_event.title, response.content.decode())

    def test__view_event_list__organised(self):
        request = self.request_factory.get(reverse('events_list'), data={'filter': 'o'})
        request.user = self.user1
        response = view_event_list(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertInHTML(self.organised_event.title, response.content.decode())

    def test__view_event_list__attending(self):
        request = self.request_factory.get(reverse('events_list'), data={'filter': 'a'})
        request.user = self.user1
        response = view_event_list(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertInHTML(self.attending_event.title, response.content.decode())

    def test__view_event_list__past(self):
        request = self.request_factory.get(reverse('events_list'), data={'filter': 'p'})
        request.user = self.user1
        response = view_event_list(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertInHTML(self.expired_event.title, response.content.decode())

    def test__view_event_list__page_not_int(self):
        request = self.request_factory.get(reverse('events_list'), data={'page': 'pageOne', 'filter': 'a'})
        request.user = self.user1
        response = view_event_list(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertInHTML(self.attending_event.title, response.content.decode())

    def test__view_event_list__page_empty(self):
        request = self.request_factory.get(reverse('events_list'), data={'page': 999, 'filter': 'a'})
        request.user = self.user1
        response = view_event_list(request, *[], **{})
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertInHTML(self.attending_event.title, response.content.decode())