import uuid
from django.db import models
from django.conf import settings
from drivers.models import DriverProfile
from vehicles.models import Vehicle, VehicleCategory
from .constants import BookingType, BookingStatus, VALID_TRANSITIONS
from common.exceptions import BookingStateError

class RideOfferStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open for Passengers'
    IN_PROGRESS = 'IN_PROGRESS', 'Trip in Progress'
    COMPLETED = 'COMPLETED', 'Trip Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'

class RideOffer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='published_rides')
    
    origin_address = models.TextField()
    origin_latitude = models.FloatField()
    origin_longitude = models.FloatField()
    
    destination_address = models.TextField()
    destination_latitude = models.FloatField()
    destination_longitude = models.FloatField()
    
    departure_datetime = models.DateTimeField()
    total_seats = models.PositiveIntegerField(default=3)
    available_seats = models.PositiveIntegerField(default=3)
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2, default=150.00)
    
    vehicle_model = models.CharField(max_length=100, default='Honda City')
    vehicle_number = models.CharField(max_length=30, default='DL-01-AB-1234')
    vehicle_category = models.CharField(max_length=20, choices=VehicleCategory.choices, default=VehicleCategory.SEDAN)
    
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=RideOfferStatus.choices, default=RideOfferStatus.OPEN)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride {self.origin_address[:15]} ➔ {self.destination_address[:15]} ({self.available_seats}/{self.total_seats} seats)"

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_reference = models.CharField(max_length=16, unique=True, editable=False)
    
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    ride_offer = models.ForeignKey(RideOffer, on_delete=models.SET_NULL, null=True, blank=True, related_name='passenger_bookings')
    seats_booked = models.PositiveIntegerField(default=1)
    
    booking_type = models.CharField(max_length=20, choices=BookingType.choices, default=BookingType.TAXI)
    vehicle_category = models.CharField(max_length=20, choices=VehicleCategory.choices, default=VehicleCategory.SEDAN)
    
    pickup_address = models.TextField()
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    
    destination_address = models.TextField()
    destination_latitude = models.FloatField()
    destination_longitude = models.FloatField()
    
    estimated_distance = models.FloatField(help_text="Distance in KM")
    estimated_duration = models.IntegerField(help_text="Duration in Minutes")
    
    estimated_fare = models.DecimalField(max_digits=10, decimal_places=2)
    final_fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    status = models.CharField(max_length=30, choices=BookingStatus.choices, default=BookingStatus.REQUESTED)
    payment_status = models.CharField(max_length=20, default='UNPAID')
    payment_method = models.CharField(max_length=30, default='CASH')
    
    cancellation_reason = models.TextField(null=True, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True, help_text="Null for immediate bookings")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def transition_to(self, new_status, reason=None):
        """Validate state transition against state machine graph."""
        allowed = VALID_TRANSITIONS.get(self.status, [])
        if new_status not in allowed and not new_status.startswith('CANCELLED'):
            raise BookingStateError(f"Invalid state transition from {self.status} to {new_status}")
            
        self.status = new_status
        if reason:
            self.cancellation_reason = reason
        self.save()

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = f"AURA-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_reference} [{self.get_status_display()}]"

