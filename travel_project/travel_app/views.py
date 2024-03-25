from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.db import models
from .models import Trip, Event
from .forms import TripForm, EventForm, CreateUserForm

def index(request):
    return render(request, 'index.html')

def user_sign_up(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')

    context = {'form': form}

    return render(request, "registration/sign-up.html", context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('login')

    return render(request, "registration/login.html")

def user_logout(request):
    logout(request)
    return redirect('login')

def contact_us(request):
    return render(request, 'contact-us.html')

def about_us(request):
    return render(request, 'aboutus.html')

@login_required(login_url='login')
def itinerary_list(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'itinerary/itinerary_list.html', {'trips': trips})

@login_required(login_url='login')
def trip_details(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    days = []
    for day_number in range(1, (trip.end_date - trip.start_date).days + 2):
        events = Event.objects.filter(trip=trip, day_number=day_number)
        days.append({'number': day_number, 'date': trip.start_date + timedelta(days=day_number - 1), 'events': events})
    return render(request, 'itinerary/trip_details.html', {'trip': trip, 'days': days})

@login_required(login_url='login')
def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect('itinerary_list')
    else:
        form = TripForm()
    return render(request, 'itinerary/create_trip.html', {'form': form})

@login_required(login_url='login')
def create_event(request, trip_id):
    trip = Trip.objects.get(pk=trip_id)
    if request.method == 'POST':
        form = EventForm(request.POST, trip=trip)
        if form.is_valid():
            event = form.save(commit=False)
            event.trip = trip
            event.save()
            return redirect('trip_details', trip_id=trip_id)
    else:
        form = EventForm(trip=trip)
    return render(request, 'itinerary/create_event.html', {'form': form})

@login_required(login_url='login')
def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    trip = event.trip
    if request.method == 'POST':
        form = EventForm(request.POST, trip=trip, instance=event)
        if form.is_valid():
            form.save()
            return redirect('trip_details', trip_id=trip.id)
    else:
        form = EventForm(trip=trip, instance=event)
    return render(request, 'itinerary/edit_event.html', {'form': form, 'event': event, 'trip': trip})

def search(request):
    return render(request, 'search.html')
