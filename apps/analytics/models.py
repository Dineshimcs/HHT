from django.db import models

class SystemDailySnapshot(models.Model):
    date = models.DateField(unique=True)
    total_bookings = models.PositiveIntegerField(default=0)
    completed_bookings = models.PositiveIntegerField(default=0)
    gross_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    platform_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Snapshot {self.date}: ₹{self.gross_revenue}"
