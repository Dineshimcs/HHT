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

    @staticmethod
    def publish_ride_offer(driver, origin_addr, origin_lat, origin_lon, drop_addr, drop_lat, drop_lon, departure_datetime, total_seats=3, price_per_seat=150.00, vehicle_model='Honda City', vehicle_number='DL-01-AB-1234', vehicle_category='SEDAN', description=''):
        from .models import RideOffer, RideOfferStatus
        offer = RideOffer.objects.create(
            driver=driver,
            origin_address=origin_addr,
            origin_latitude=origin_lat,
            origin_longitude=origin_lon,
            destination_address=drop_addr,
            destination_latitude=drop_lat,
            destination_longitude=drop_lon,
            departure_datetime=departure_datetime,
            total_seats=total_seats,
            available_seats=total_seats,
            price_per_seat=price_per_seat,
            vehicle_model=vehicle_model,
            vehicle_number=vehicle_number,
            vehicle_category=vehicle_category,
            description=description,
            status=RideOfferStatus.OPEN
        )
        return offer

    @staticmethod
    def book_seat_in_offer(ride_offer_id, customer, seats_booked=1):
        from .models import RideOffer, Booking
        from drivers.models import DriverProfile
        with transaction.atomic():
            offer = RideOffer.objects.select_for_update().get(id=ride_offer_id)
            if offer.available_seats < seats_booked:
                raise ValueError("Not enough seats available for this ride offer.")
            
            offer.available_seats -= seats_booked
            offer.save()

            distance_km = calculate_haversine_distance(
                offer.origin_latitude, offer.origin_longitude,
                offer.destination_latitude, offer.destination_longitude
            )
            duration_mins = max(5, int(distance_km * 2.5) + 5)
            total_fare = offer.price_per_seat * seats_booked

            # Get or create driver profile for the offering driver
            driver_profile, _ = DriverProfile.objects.get_or_create(
                user=offer.driver,
                defaults={'license_number': f"LIC-{offer.driver.id:06d}"}
            )

            booking = Booking.objects.create(
                customer=customer,
                driver=driver_profile,
                ride_offer=offer,
                seats_booked=seats_booked,
                booking_type=BookingType.CARPOOL if hasattr(BookingType, 'CARPOOL') else 'CARPOOL',
                vehicle_category=offer.vehicle_category,
                pickup_address=offer.origin_address,
                pickup_latitude=offer.origin_latitude,
                pickup_longitude=offer.origin_longitude,
                destination_address=offer.destination_address,
                destination_latitude=offer.destination_latitude,
                destination_longitude=offer.destination_longitude,
                estimated_distance=distance_km,
                estimated_duration=duration_mins,
                estimated_fare=total_fare,
                final_fare=total_fare,
                status=BookingStatus.DRIVER_ASSIGNED,
                scheduled_at=offer.departure_datetime
            )
            return booking

