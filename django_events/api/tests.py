from datetime import datetime, timedelta
from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_202_ACCEPTED

from events.models import Event


def get_url(view_name, args=None):
    """
    Convenient wrapper around reverse() and ensures that the path's have a trailing slash to avoid a 301 status code
    """
    url = reverse(view_name, args=args)
    if not url.endswith('/'):
        url += '/'
    return url


class TestApi(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(email='user1@events.com', password='password')
        self.user2 = get_user_model().objects.create_user(email='user2@events.com', password='password')
        self.organised_event_dt = datetime.now() + timedelta(hours=2)
        self.organised_event = Event.objects.create(title='Organised Event 1',
                                                    description='Event Desc. 1',
                                                    date_time=self.organised_event_dt,
                                                    organiser=self.user1)

        self.organised_event.attendees.add(self.user2)
        self.organised_event.save()

        self.attending_event_dt = datetime.now() + timedelta(hours=2)
        self.attending_event = Event.objects.create(title='Attending Event 1',
                                                    description='Event Desc. 1',
                                                    date_time=self.attending_event_dt,
                                                    organiser=self.user2)
        self.attending_event.attendees.add(self.user1)
        self.attending_event.save()

        self.not_attending_event_dt = datetime.now() + timedelta(hours=2)
        self.not_attending_event = Event.objects.create(title='Not Attending Event 1',
                                                        description='Event Desc. 1',
                                                        date_time=self.attending_event_dt,
                                                        organiser=self.user2)
        self.not_attending_event.attendees.add(self.user2)
        self.not_attending_event.save()

        self.expired_event_dt = datetime.now() - timedelta(hours=4)
        self.expired_event = Event.objects.create(title='Passed Event 1',
                                                  description='Event Desc. 1',
                                                  date_time=self.expired_event_dt,
                                                  organiser=self.user1)

        self.user1_client = APIClient()
        self.user1_client.force_authenticate(user=self.user1)

    def test_event_list(self):
        response = self.user1_client.get('/api/event/', {}, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data.get('results')), 3)

        expected_evt1 = {'id': 1,
                         'title': 'Organised Event 1',
                         'description': 'Event Desc. 1',
                         'date_time': self.organised_event_dt.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                         'attendees_count': 1,
                         'organiser_friendly_name': 'user1',
                         'organiser': 'user1@events.com',
                         'url': 'http://testserver/api/event/1/'}
        actual_evt1 = data['results'][0]
        actual_evt1['url'] = str(actual_evt1['url'])
        self.assertDictEqual(dict(actual_evt1), expected_evt1)

        expected_evt2 = {'id': 2,
                         'title': 'Attending Event 1',
                         'description': 'Event Desc. 1',
                         'date_time': self.attending_event_dt.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                         'attendees_count': 1,
                         'organiser_friendly_name': 'user2',
                         'organiser': 'user2@events.com',
                         'url': 'http://testserver/api/event/2/'}
        actual_evt2 = data['results'][1]
        actual_evt2['url'] = str(actual_evt2['url'])

        self.assertDictEqual(dict(actual_evt2), expected_evt2)

    def test_event_detail_invalid_event(self):
        response = self.user1_client.get(get_url('event-detail', args=(8458546, )), {}, format='json', secure=True)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_event_detail_correct(self):
        response = self.user1_client.get(get_url('event-detail', args=(self.organised_event.id, )), {}, format='json', secure=False)
        self.assertEqual(response.status_code, HTTP_200_OK)

        actual = response.data
        expected = {'id': 1,
                    'title': 'Organised Event 1',
                    'description': 'Event Desc. 1',
                    'date_time': self.organised_event_dt.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                    'organiser_friendly_name': 'user1',
                    'organiser': 'user1@events.com',
                    'attendees': [{'email': 'user2@events.com', 'friendly_name': 'user2'}],
                    'is_organiser': True,
                    'is_in_past': False,
                    'is_attending': False}
        self.assertDictEqual(actual, expected)

    def test_attend_invalid_event(self):
        response = self.user1_client.post(get_url('event-attend', args=(7686867876876867,)), {}, format='json')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_attend_event_in_past(self):
        response = self.user1_client.post(get_url('event-attend', args=(self.expired_event.id,)), {}, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_attend_event_correct(self):
        response = self.user1_client.post(get_url('event-attend', args=(self.not_attending_event.id,)), {}, format='json')
        self.assertEqual(response.status_code, HTTP_202_ACCEPTED)

    def test_unattend_invalid_event(self):
        response = self.user1_client.post(get_url('event-unattend', args=(7686867876876867,)), {}, format='json')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_unattend_event_in_past(self):
        response = self.user1_client.post(get_url('event-unattend', args=(self.expired_event.id,)), {}, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_unattend_event_correct(self):
        response = self.user1_client.post(get_url('event-unattend', args=(self.attending_event.id,)), {},
                                          format='json')
        self.assertEqual(response.status_code, HTTP_202_ACCEPTED)

    def test_update_not_organiser(self):
        response = self.user1_client.put(get_url('event-detail', args=(self.attending_event.id,)),
                                         {'date_time': '2020-07-08T00:41:51.746287',
                                          'title': 'title',
                                          'description': 'description'},
                                         format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
