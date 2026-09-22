from django.urls import path
from . import views

app_name = 'trips'

urlpatterns = [
    path('api/<uuid:booking_id>/start/', views.api_start_trip, name='api_start_trip'),
    path('api/<uuid:booking_id>/complete/', views.api_complete_trip, name='api_complete_trip'),
]
