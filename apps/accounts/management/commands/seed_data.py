from decimal import Decimal
from django.core.management.base import BaseCommand
from accounts.models import User
from drivers.models import DriverProfile
from customers.models import CustomerProfile
from vehicles.models import Vehicle, VehicleCategory
from pricing.models import PricingRule
from bookings.models import Booking
from bookings.constants import BookingStatus

class Command(BaseCommand):
    help = 'Seeds initial demonstration data for AURA Mobility platform'

    def handle(self, *args, **options):
        self.stdout.write("Seeding AURA Mobility initial data...")

        # 1. Create Default Pricing Rules
        rules_data = [
            (VehicleCategory.SEDAN, Decimal('60.00'), Decimal('14.00'), Decimal('2.00'), Decimal('120.00')),
            (VehicleCategory.SUV, Decimal('100.00'), Decimal('20.00'), Decimal('3.00'), Decimal('200.00')),
            (VehicleCategory.PREMIUM, Decimal('180.00'), Decimal('28.00'), Decimal('5.00'), Decimal('450.00')),
            (VehicleCategory.CHAUFFEUR, Decimal('250.00'), Decimal('0.00'), Decimal('4.00'), Decimal('350.00')),
        ]
        for cat, base, per_km, per_min, min_fare in rules_data:
            PricingRule.objects.get_or_create(
                category=cat,
                defaults={
                    'base_fare': base,
                    'per_km_rate': per_km,
                    'per_minute_rate': per_min,
                    'minimum_fare': min_fare
                }
            )

        # 2. Create Demo Admin User
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@auramobility.com',
                'first_name': 'Operations',
                'last_name': 'Admin',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        # 3. Create Demo Customer User
        customer_user, _ = User.objects.get_or_create(
            username='customer',
            defaults={
                'email': 'customer@auramobility.com',
                'first_name': 'Vikram',
                'last_name': 'Sharma',
                'phone': '+919876543210',
                'role': User.Role.CUSTOMER
            }
        )
        customer_user.set_password('customer123')
        customer_user.save()
        CustomerProfile.objects.get_or_create(user=customer_user)

        # 4. Create Demo Driver User
        driver_user, _ = User.objects.get_or_create(
            username='driver',
            defaults={
                'email': 'driver@auramobility.com',
                'first_name': 'Rajesh',
                'last_name': 'Kumar',
                'phone': '+919876543211',
                'role': User.Role.DRIVER
            }
        )
        driver_user.set_password('driver123')
        driver_user.save()
        
        driver_profile, _ = DriverProfile.objects.get_or_create(
            user=driver_user,
            defaults={
                'license_number': 'DL-042021009876',
                'verification_status': DriverProfile.VerificationStatus.VERIFIED,
                'is_online': True,
                'rating': Decimal('4.90'),
                'total_trips': 1240
            }
        )

        # 5. Create Vehicle
        Vehicle.objects.get_or_create(
            registration_number='DL-01-AB-1234',
            defaults={
                'driver': driver_profile,
                'category': VehicleCategory.SEDAN,
                'make': 'Honda',
                'model': 'City',
                'year': 2023,
                'color': 'White',
                'is_active': True,
                'is_verified': True
            }
        )

        # 6. Create Demo Booking
        Booking.objects.get_or_create(
            booking_reference='AURA-8F92A1',
            defaults={
                'customer': customer_user,
                'driver': driver_profile,
                'vehicle_category': VehicleCategory.SEDAN,
                'pickup_address': 'Connaught Place, Inner Circle, New Delhi',
                'pickup_latitude': 28.6315,
                'pickup_longitude': 77.2167,
                'destination_address': 'IGI Airport Terminal 3, New Delhi',
                'destination_latitude': 28.5562,
                'destination_longitude': 77.1000,
                'estimated_distance': 15.2,
                'estimated_duration': 32,
                'estimated_fare': Decimal('280.00'),
                'status': BookingStatus.TRIP_IN_PROGRESS,
                'payment_method': 'CASH'
            }
        )

        self.stdout.write(self.style.SUCCESS("Data seeding completed successfully!"))
