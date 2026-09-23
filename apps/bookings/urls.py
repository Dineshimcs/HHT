from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/', views.create_booking_view, name='create'),
    path('offer-ride/', views.offer_ride_view, name='offer_ride'),
    path('book-seat/<uuid:offer_id>/', views.book_carpool_seat_view, name='book_seat'),
    path('cancel/<uuid:booking_id>/', views.cancel_booking_view, name='cancel'),
    path('<uuid:booking_id>/', views.booking_detail_view, name='detail'),
    path('api/fare-estimate/', views.api_fare_estimate, name='api_fare_estimate'),
]

