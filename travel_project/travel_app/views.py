from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    return render(request,'index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            first_name = user.first_name

            return render(request, "index.html", {"first_name": first_name})
        else:
            messages.error(request, "Wrong Credentials! Please sign-in again.")
            return redirect('home')

    return render(request, "registration/login.html")
