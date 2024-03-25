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

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['day_number', 'event_title', 'time', 'description', 'link']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'})
        }