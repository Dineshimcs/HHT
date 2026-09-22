from django.utils import timezone
from django.db import transaction
from bookings.models import Booking
from bookings.constants import BookingStatus
from pricing.services import PricingService
from .models import Trip

class TripService:
    @staticmethod
    def mark_driver_arrived(booking_id):
        with transaction.atomic():
            booking = Booking.objects.select_for_update().get(id=booking_id)
            booking.transition_to(BookingStatus.DRIVER_ARRIVED)
            trip, _ = Trip.objects.get_or_create(booking=booking)
            trip.driver_arrived_at = timezone.now()
            trip.save()
            return booking

    @staticmethod
    def start_trip(booking_id, otp=None):
        with transaction.atomic():
            booking = Booking.objects.select_for_update().get(id=booking_id)
            booking.transition_to(BookingStatus.TRIP_STARTED)
            booking.transition_to(BookingStatus.TRIP_IN_PROGRESS)
            
            trip, _ = Trip.objects.get_or_create(booking=booking)
            trip.started_at = timezone.now()
            trip.save()
            return booking

    @staticmethod
    def complete_trip(booking_id, actual_distance_km=None):
        with transaction.atomic():
            booking = Booking.objects.select_for_update().get(id=booking_id)
            dist = actual_distance_km or booking.estimated_distance
            
            # Recalculate final fare
            final_fare = PricingService.calculate_fare(
                booking.vehicle_category,
                dist,
                booking.estimated_duration
            )
            
            booking.final_fare = final_fare
            booking.transition_to(BookingStatus.TRIP_COMPLETED)
            booking.transition_to(BookingStatus.PAYMENT_PENDING)
            
            trip, _ = Trip.objects.get_or_create(booking=booking)
            trip.completed_at = timezone.now()
            trip.actual_distance_km = dist
            trip.save()
            
            if booking.driver:
                booking.driver.is_busy = False
                booking.driver.save()
                
            return booking
