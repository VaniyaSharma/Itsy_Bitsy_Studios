from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

from django.contrib.auth.decorators import login_required

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


def search(request):
    return render(request, 'search.html')


# login_required(login_url='login')
def itinerary(request):
    return render(request, 'itinerary.html')
