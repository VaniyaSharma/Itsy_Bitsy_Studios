from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

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


def search(request):
    return render(request, 'search.html')


def itinerary(request):
    return render(request, 'itinerary.html')
