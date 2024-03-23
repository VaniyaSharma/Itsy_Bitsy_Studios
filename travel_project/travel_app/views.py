from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import models
from .models import Day
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

def itinerary (request):
    form = EventForm()
    return render(request, 'itinerary.html', {'form': form})

def create_event(request, day_id):
    day = get_object_or_404(Day, pk=day_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.day = day
            event.save()
            return redirect('day_detail', day_id=day_id)
    else:
        form = EventForm()
    return render(request, 'itinerary.html', {'form': form})

def search(request):
    return render(request, 'search.html')

