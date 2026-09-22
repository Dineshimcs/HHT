from django.db import models
from bookings.models import Booking

class Trip(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='trip_detail')
    driver_arrived_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    actual_distance_km = models.FloatField(default=0.0)
    actual_duration_mins = models.PositiveIntegerField(default=0)
    start_otp = models.CharField(max_length=6, default='1234')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trip for Booking: {self.booking.booking_reference}"
