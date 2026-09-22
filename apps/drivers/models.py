from django.db import models
from django.conf import settings

class DriverProfile(models.Model):
    class VerificationStatus(models.TextChoices):
        UNVERIFIED = 'UNVERIFIED', 'Unverified'
        PENDING = 'PENDING', 'Pending Review'
        VERIFIED = 'VERIFIED', 'Verified & Active'
        REJECTED = 'REJECTED', 'Rejected'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry = models.DateField(null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.UNVERIFIED)
    
    is_online = models.BooleanField(default=False)
    is_busy = models.BooleanField(default=False)
    
    current_latitude = models.FloatField(default=28.6139) # Default GPS
    current_longitude = models.FloatField(default=77.2090)
    last_location_update = models.DateTimeField(auto_now=True)
    
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    total_trips = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_eligible_for_dispatch(self):
        return self.is_online and not self.is_busy and self.verification_status == self.VerificationStatus.VERIFIED

    def __str__(self):
        return f"Driver: {self.user.get_full_name() or self.user.username} [{self.get_verification_status_display()}]"
