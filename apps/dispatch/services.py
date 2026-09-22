from django.db import transaction
from drivers.models import DriverProfile
from bookings.models import Booking
from bookings.constants import BookingStatus
from common.utilities import calculate_haversine_distance
from common.exceptions import DriverNotAvailableError, BookingStateError

class DispatchService:
    @staticmethod
    def find_eligible_drivers(pickup_lat, pickup_lon, radius_km=10.0):
        """
        Find online, verified, non-busy drivers within geofence radius.
        Rank candidates by distance and rating.
        """
        candidates = DriverProfile.objects.filter(
            is_online=True,
            is_busy=False,
            verification_status=DriverProfile.VerificationStatus.VERIFIED
        )

        eligible = []
        for driver in candidates:
            dist = calculate_haversine_distance(
                pickup_lat, pickup_lon,
                driver.current_latitude, driver.current_longitude
            )
            if dist <= radius_km:
                # Rank score formula: higher rating + closer proximity
                score = (float(driver.rating) * 20.0) - (dist * 2.0)
                eligible.append((driver, dist, score))

        # Sort by score descending
        eligible.sort(key=lambda x: x[2], reverse=True)
        return [item[0] for item in eligible]

    @staticmethod
    def assign_driver_atomically(booking_id, driver):
        """
        Atomically assign driver to booking using select_for_update to prevent race conditions.
        """
        with transaction.atomic():
            booking = Booking.objects.select_for_update().get(id=booking_id)
            if booking.driver is not None:
                raise BookingStateError("Booking has already been assigned to another driver.")

            driver_profile = DriverProfile.objects.select_for_update().get(id=driver.id)
            if driver_profile.is_busy:
                raise DriverNotAvailableError("Driver is currently busy with another ride.")

            booking.driver = driver_profile
            booking.status = BookingStatus.DRIVER_ASSIGNED
            booking.save()

            driver_profile.is_busy = True
            driver_profile.save()

            return booking

