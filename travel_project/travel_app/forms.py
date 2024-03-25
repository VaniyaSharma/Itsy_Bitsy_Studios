from django import forms
from .models import Trip, Event
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['name', 'location', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['day_number', 'event_title', 'time', 'description', 'link']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'})
        }

    def __init__(self, *args, **kwargs):
        trip = kwargs.pop('trip')
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['day_number'] = forms.ChoiceField(
            choices=[(day, f'Day {day}') for day in range(1, trip.duration + 1)]
        )