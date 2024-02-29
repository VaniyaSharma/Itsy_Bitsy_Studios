from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    return render(request,'index.html')

def user_sign_up(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['pass']
        confirmPass = request.POST['confirmPass']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('sign-up')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('sign-up')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('sign-up')

        if password != confirmPass:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('sign-up')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('sign-up')

        newuser = User.objects.create_user(username, email, password)
        newuser.first_name = first_name
        newuser.last_name = last_name
        newuser.is_active = False
        newuser.save()

    return render(request, "registration/sign-up.html")

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
            messages.error(request, "Wrong Credentials!!")
            return redirect('home')

    return render(request, "registration/login.html")