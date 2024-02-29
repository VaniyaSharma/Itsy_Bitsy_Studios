from django.urls import path
from .views import index
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('login/', views.user_login, name='login'),
]
