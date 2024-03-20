import threading

from Tools.scripts import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from Itsy_Bitsy_Studios.travel_project.travel_project import settings


# Create your views here.

def index(request):
    return render(request,'index.html')


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_page = get_current_site(request)
    email_sub = 'Activate your account'
    email_content = render_to_string('registration/activate_email.html', {
        'user': user,
        'domain': current_page,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_sub, body=email_content,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    if not settings.TESTING:
        EmailThread(email).start()

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

        if not messages.error['has_error']:
            send_activation_email(user, request)

            messages.add_message(request, messages.SUCCESS,
                                 'We sent you an email to verify your account')

        return redirect('login')

    return render(request, "registration/sign-up.html")

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']

        user = authenticate(username=username, password=password)

        if user and not user.is_email_verified:
            messages.add_message(request, messages.ERROR,
                                 'Email is not verified, please check your email inbox')
            return render(request, 'registration/login.html')

        if user is not None:
            login(request, user)
            first_name = user.first_name

            return render(request, "index.html", {"first_name": first_name})
        else:
            messages.error(request, "Wrong Credentials! Please try again :)")
            return redirect('home')


    return render(request, "registration/login.html")
def contact_us (request):
    return render(request,'contact-us.html')

def about_us (request):
    return render(request, 'aboutus.html')