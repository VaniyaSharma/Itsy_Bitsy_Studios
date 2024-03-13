from django.urls import path
from .views import index
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('sign-up/', views.user_sign_up, name='sign-up'),
    path('login/', views.user_login, name='login'),
    path('contact-us/',views.contact_us, name='contact-us')
]

