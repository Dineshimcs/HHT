from django.db import models

class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    max_discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=100.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Coupon: {self.code} ({self.discount_percent}% off)"
