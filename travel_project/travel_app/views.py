from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import models
from .models import Trip, Itinerary, Event
from .forms import EventForm, CreateUserForm

def index(request):
    return render(request, 'index.html')

def user_sign_up(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}

    return render(request, "registration/sign-up.html", context)

def user_login(request):
    return render(request, "registration/login.html")

def user_logout(request):
    logout(request)
    return redirect('index')

def contact_us(request):
    return render(request, 'contact-us.html')

def about_us(request):
    return render(request, 'aboutus.html')

def itinerary_list (request):
    return render(request, 'itinerary/itinerary_list.html')

def create_event(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            day_number = int(request.POST['day_number'])
            event = form.save(commit=False)
            event.save()
            itinerary, created = Itinerary.objects.get_or_create(trip=trip, day_number=day_number)
            itinerary.events.add(event)
            return redirect('itinerary_list')
    else:
        form = EventForm()
    return render(request, 'itinerary/create_event.html', {'form': form, 'trip': trip})

def edit_event(request, event_id):
    event - Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('itinerary_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'itinerary/edit_event.html', {'form': form, 'event': event})

def search(request):
    return render(request, 'search.html')

