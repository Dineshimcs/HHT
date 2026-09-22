from django.db import models
from django.conf import settings
from bookings.models import Booking

class Rating(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='rating_entry')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_ratings')
    score = models.PositiveSmallIntegerField(default=5) # 1 to 5
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.score}★ for Booking {self.booking.booking_reference}"
