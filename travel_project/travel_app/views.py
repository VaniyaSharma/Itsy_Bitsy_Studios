from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout



from django.db import models

from travel_project import settings


# Create your models here.


def index(request):
    return render(request,'index.html')



def user_sign_up(request):

    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirmPass = request.POST['confirmPass']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('index')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('index')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('index')

        if password != confirmPass:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('index')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('index')

        newuser = User.objects.create_user(username, email, password)
        newuser.first_name = first_name
        newuser.last_name = last_name
        newuser.is_active = False
        newuser.save()

        print("New User:", newuser.username, newuser.email, newuser.password)

        messages.success(request,"Your account has been succesfully created!")

        # Welcome email

        subject = "Welcome to Tripsee!!"
        message= "Hello" + newuser.first_name + "!\n" + "Thank you for registering on our website. We are so excited to have you with us. \n" + "Please check your email for account confirmation to login and start planning your trip! \n\n" + "Thank you.\n With regards, \n Tripsee team"
        from_email = settings.EMAIL_HOST_USER

        to_user = [newuser.email]
        send_mail(subject, message, from_email, to_user, fail_silently=True)



        return redirect('login')

    return render(request, "registration/sign-up.html")

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print("Username:", username)  # Debugging statement
        print("Password:", password)  # Debugging statement

        user = authenticate(username=username, password=password)
        
        user = User.objects.filter(username=username).first()
        if user is None:
            print("User does not exist:", username)

        print("Authenticated User:", user)

        if user is not None:
            login(request, user)
            first_name = user.first_name

            return render(request, "index.html", {"first_name": first_name})
        else:
            messages.error(request, "Wrong Credentials! Please try again :)")
            return redirect('index')


    return render(request, "registration/login.html")

def user_logout(request):
    logout(request)
    # Redirect to home or login page after logout
    return redirect('index')

def contact_us (request):
    return render(request,'contact-us.html')

def about_us (request):
    return render(request, 'aboutus.html')

def search (request):
    return render(request,'search.html')

def itinerary (request):
    return render(request, 'itinerary.html')

