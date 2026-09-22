from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        DRIVER = 'DRIVER', 'Driver'
        ADMIN = 'ADMIN', 'Admin / Operations'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_customer_role(self):
        return self.role == self.Role.CUSTOMER

    def is_driver_role(self):
        return self.role == self.Role.DRIVER

    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
