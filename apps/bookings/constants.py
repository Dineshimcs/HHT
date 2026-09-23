from django.db import models

class BookingType(models.TextChoices):
    TAXI = 'TAXI', 'Taxi / Full Vehicle Booking'
    DRIVER_ONLY = 'DRIVER_ONLY', 'Professional Driver Rental (Customer Vehicle)'
    CARPOOL = 'CARPOOL', 'Carpool / Shared Ride'


class BookingStatus(models.TextChoices):
    REQUESTED = 'REQUESTED', 'Requested'
    SEARCHING_DRIVER = 'SEARCHING_DRIVER', 'Searching Nearby Drivers'
    DRIVER_ASSIGNED = 'DRIVER_ASSIGNED', 'Driver Assigned'
    DRIVER_ACCEPTED = 'DRIVER_ACCEPTED', 'Driver Accepted'
    DRIVER_ARRIVING = 'DRIVER_ARRIVING', 'Driver En Route to Pickup'
    DRIVER_ARRIVED = 'DRIVER_ARRIVED', 'Driver Arrived at Pickup'
    TRIP_STARTED = 'TRIP_STARTED', 'Trip Started'
    TRIP_IN_PROGRESS = 'TRIP_IN_PROGRESS', 'Trip in Progress'
    TRIP_COMPLETED = 'TRIP_COMPLETED', 'Trip Completed'
    PAYMENT_PENDING = 'PAYMENT_PENDING', 'Payment Pending'
    PAYMENT_COMPLETED = 'PAYMENT_COMPLETED', 'Payment Completed'
    RATED = 'RATED', 'Rated & Closed'
    
    # Failure / Cancellation states
    CANCELLED_BY_CUSTOMER = 'CANCELLED_BY_CUSTOMER', 'Cancelled by Customer'
    CANCELLED_BY_DRIVER = 'CANCELLED_BY_DRIVER', 'Cancelled by Driver'
    CANCELLED_BY_ADMIN = 'CANCELLED_BY_ADMIN', 'Cancelled by Admin'
    DRIVER_TIMEOUT = 'DRIVER_TIMEOUT', 'Driver Request Timeout'
    NO_DRIVER_AVAILABLE = 'NO_DRIVER_AVAILABLE', 'No Drivers Available'
    PAYMENT_FAILED = 'PAYMENT_FAILED', 'Payment Failed'

VALID_TRANSITIONS = {
    BookingStatus.REQUESTED: [BookingStatus.SEARCHING_DRIVER, BookingStatus.CANCELLED_BY_CUSTOMER],
    BookingStatus.SEARCHING_DRIVER: [BookingStatus.DRIVER_ASSIGNED, BookingStatus.NO_DRIVER_AVAILABLE, BookingStatus.CANCELLED_BY_CUSTOMER],
    BookingStatus.DRIVER_ASSIGNED: [BookingStatus.DRIVER_ACCEPTED, BookingStatus.DRIVER_TIMEOUT, BookingStatus.CANCELLED_BY_CUSTOMER, BookingStatus.CANCELLED_BY_DRIVER],
    BookingStatus.DRIVER_ACCEPTED: [BookingStatus.DRIVER_ARRIVING, BookingStatus.CANCELLED_BY_CUSTOMER, BookingStatus.CANCELLED_BY_DRIVER],
    BookingStatus.DRIVER_ARRIVING: [BookingStatus.DRIVER_ARRIVED, BookingStatus.CANCELLED_BY_CUSTOMER, BookingStatus.CANCELLED_BY_DRIVER],
    BookingStatus.DRIVER_ARRIVED: [BookingStatus.TRIP_STARTED, BookingStatus.CANCELLED_BY_CUSTOMER, BookingStatus.CANCELLED_BY_DRIVER],
    BookingStatus.TRIP_STARTED: [BookingStatus.TRIP_IN_PROGRESS, BookingStatus.CANCELLED_BY_ADMIN],
    BookingStatus.TRIP_IN_PROGRESS: [BookingStatus.TRIP_COMPLETED, BookingStatus.CANCELLED_BY_ADMIN],
    BookingStatus.TRIP_COMPLETED: [BookingStatus.PAYMENT_PENDING, BookingStatus.PAYMENT_COMPLETED],
    BookingStatus.PAYMENT_PENDING: [BookingStatus.PAYMENT_COMPLETED, BookingStatus.PAYMENT_FAILED],
    BookingStatus.PAYMENT_COMPLETED: [BookingStatus.RATED],
}
