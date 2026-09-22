from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/', views.create_booking_view, name='create'),
    path('<uuid:booking_id>/', views.booking_detail_view, name='detail'),
    path('api/fare-estimate/', views.api_fare_estimate, name='api_fare_estimate'),
]
