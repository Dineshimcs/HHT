from django.db import models
from drivers.models import DriverProfile

class VehicleCategory(models.TextChoices):
    SEDAN = 'SEDAN', 'Economy Sedan (4 Seats)'
    SUV = 'SUV', 'Executive SUV (6 Seats)'
    PREMIUM = 'PREMIUM', 'Luxury Executive (4 Seats)'
    CHAUFFEUR = 'CHAUFFEUR', 'Driver Rental Only (Customer Car)'

class Vehicle(models.Model):
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='vehicles')
    category = models.CharField(max_length=20, choices=VehicleCategory.choices, default=VehicleCategory.SEDAN)
    registration_number = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=50) # Toyota, Honda, Hyundai
    model = models.CharField(max_length=50) # City, Innova, Verna
    year = models.PositiveIntegerField(default=2022)
    color = models.CharField(max_length=30, default='White')
    seating_capacity = models.PositiveIntegerField(default=4)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.make} {self.model} [{self.registration_number}] ({self.get_category_display()})"

class VehicleDocument(models.Model):
    class DocType(models.TextChoices):
        RC = 'RC', 'Registration Certificate'
        INSURANCE = 'INSURANCE', 'Vehicle Insurance'
        PERMIT = 'PERMIT', 'Commercial Driving Permit'
        FITNESS = 'FITNESS', 'Fitness Certificate'

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DocType.choices)
    document_number = models.CharField(max_length=50)
    file = models.FileField(upload_to='vehicle_docs/', null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_doc_type_display()} for {self.vehicle.registration_number}"
