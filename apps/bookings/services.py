from django.db import transaction
from .models import Booking
from .constants import BookingStatus, BookingType
from pricing.services import PricingService
from dispatch.services import DispatchService
from common.utilities import calculate_haversine_distance

class BookingService:
    @staticmethod
    def create_booking(customer, pickup_addr, pickup_lat, pickup_lon, drop_addr, drop_lat, drop_lon, vehicle_category, booking_type=BookingType.TAXI, scheduled_at=None):
        """
        Create a new booking, estimate distance & fare, and trigger initial dispatch if instant ride.
        """
        distance_km = calculate_haversine_distance(pickup_lat, pickup_lon, drop_lat, drop_lon)
        # Rough estimated duration: 2.5 mins per km + 5 mins base traffic
        duration_mins = max(5, int(distance_km * 2.5) + 5)
        
        estimated_fare = PricingService.calculate_fare(vehicle_category, distance_km, duration_mins)
        
        with transaction.atomic():
            booking = Booking.objects.create(
                customer=customer,
                booking_type=booking_type,
                vehicle_category=vehicle_category,
                pickup_address=pickup_addr,
                pickup_latitude=pickup_lat,
                pickup_longitude=pickup_lon,
                destination_address=drop_addr,
                destination_latitude=drop_lat,
                destination_longitude=drop_lon,
                estimated_distance=distance_km,
                estimated_duration=duration_mins,
                estimated_fare=estimated_fare,
                status=BookingStatus.REQUESTED,
                scheduled_at=scheduled_at
            )
            
            if not scheduled_at:
                booking.transition_to(BookingStatus.SEARCHING_DRIVER)
                # Attempt instant dispatch lookup
                eligible = DispatchService.find_eligible_drivers(pickup_lat, pickup_lon)
                if eligible:
                    DispatchService.assign_driver_atomically(booking.id, eligible[0])

        return booking

    @staticmethod
    def cancel_booking(booking_id, cancelled_by_user, reason="User cancelled"):
        with transaction.atomic():
            booking = Booking.objects.select_for_update().get(id=booking_id)
            if cancelled_by_user.is_driver_role():
                booking.transition_to(BookingStatus.CANCELLED_BY_DRIVER, reason=reason)
            elif cancelled_by_user.is_admin_role():
                booking.transition_to(BookingStatus.CANCELLED_BY_ADMIN, reason=reason)
            else:
                booking.transition_to(BookingStatus.CANCELLED_BY_CUSTOMER, reason=reason)

            if booking.driver:
                booking.driver.is_busy = False
                booking.driver.save()

            return booking
