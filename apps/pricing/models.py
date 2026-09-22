from django.db import models
from vehicles.models import VehicleCategory

class PricingRule(models.Model):
    category = models.CharField(max_length=20, choices=VehicleCategory.choices, unique=True)
    base_fare = models.DecimalField(max_digits=8, decimal_places=2, default=60.00)
    per_km_rate = models.DecimalField(max_digits=8, decimal_places=2, default=14.00)
    per_minute_rate = models.DecimalField(max_digits=8, decimal_places=2, default=2.00)
    minimum_fare = models.DecimalField(max_digits=8, decimal_places=2, default=120.00)
    surge_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    night_charge_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    platform_commission_percent = models.DecimalField(max_digits=5, decimal_places=2, default=15.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pricing Rule: {self.get_category_display()} (Base: ₹{self.base_fare})"
