from django.db import models
from django.conf import settings

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    profile_photo = models.ImageField(upload_to='customers/photos/', null=True, blank=True)
    default_payment_method = models.CharField(max_length=50, default='CASH')
    total_rides = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Customer: {self.user.get_full_name() or self.user.username}"

class CustomerAddress(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=50) # Home, Work, Favorite
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label}: {self.address[:30]}"
