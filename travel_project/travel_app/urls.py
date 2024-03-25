from django.urls import path
from .views import index
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('sign-up/', views.user_sign_up, name='sign-up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('contact-us/',views.contact_us, name='contact-us'),
    path('search/', views.search, name='search'),
    path('aboutus/', views.about_us, name="aboutus"),
    path('itinerary/itinerary_list', views.itinerary_list, name="itinerary_list"),
    path('trip/<int:trip_id>/', views.trip_details, name='trip_detail'),
    path('create_trip/', views.create_trip, name='create_trip'),
    path('trip/<int:trip_id>/create_event/', views.create_event, name='create_event')
]

