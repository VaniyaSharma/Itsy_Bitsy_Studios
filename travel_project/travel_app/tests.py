from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Trip, Event

class CreateTripTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_trip_view(self):
        response = self.client.post(reverse('create_trip'), {'name': 'New Trip', 'location': 'New Location', 'start_date': '2024-04-01', 'end_date': '2024-04-05'})
        self.assertEqual(response.status_code, 302)  # Check for redirection after successful form submission
        self.assertTrue(Trip.objects.filter(name='New Trip').exists())

class CreateEventTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.trip = Trip.objects.create(user=self.user, name='Test Trip', location='Test Location', start_date='2024-03-01', end_date='2024-03-05')
        self.client.login(username='testuser', password='12345')

    def test_create_event_view(self):
        response = self.client.post(reverse('create_event', kwargs={'trip_id': self.trip.id}), {'day_number': 1, 'event_title': 'New Event', 'time': '08:00'})
        self.assertEqual(response.status_code, 302)  # Check for redirection after successful form submission
        self.assertTrue(Event.objects.filter(trip=self.trip, event_title='New Event').exists())
