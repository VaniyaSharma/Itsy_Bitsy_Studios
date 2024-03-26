from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.db import models
from .models import Trip, Event, Location

from .models import Trip, Event
from .forms import TripForm, EventForm, CreateUserForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def index(request):
    return render(request, 'index.html')

def user_sign_up(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, 'Hi ' + user + '! '+ 'your account was created! Please check your email for confirmationa and login link!')

            template = render_to_string('registration/email.html', {'name': user})

            email = EmailMessage(
                'Thank you for registering with Tripsee!',
                template,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email.fail_silently = False
            email.send()

            return redirect('index')

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
    initial_data = {}
    property_value = request.GET.get('property_value')
    if property_value:
        initial_data['location'] = Location.objects.get(name=property_value)
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect('itinerary_list')
    else:
        form = TripForm(initial=initial_data)
    return render(request, 'itinerary/create_trip.html', {'form': form})

def delete_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    if request.method == 'POST':
        trip.delete()
        return redirect('itinerary_list')

    return render(request, 'itinerary/delete_trip.html', {'trip': trip})

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

def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('trip_details', trip_id=event.trip.id)

    return render(request, 'itinerary/delete_event.html', {'event': event})

def search(request):
    return render(request, 'search.html')

def location_detail_with_id(request, location_id):
    location = get_object_or_404(Location, id=location_id)

    return render(request, 'location_details.html',{'location': location})

def search_location(request):
    locations = Location.objects.all()
    query = request.GET.get('query', '')
    if query.strip():  
        locations = locations.filter(name__icontains=query)
    return render(request, 'search.html', {'locations': locations})

def get_location_id_from_query(query):
    try:
        location = Location.objects.get(name__icontains=query)
        return location.id
    except Location.DoesNotExist:
        return None

