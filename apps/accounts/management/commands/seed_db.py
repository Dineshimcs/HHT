import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from drivers.models import DriverProfile
from customers.models import CustomerProfile
from bookings.models import RideOffer, Booking, RideOfferStatus, BookingStatus, BookingType

User = get_user_model()

class Command(BaseCommand):
    help = "Seed database with sample BlaBlaCar carpool ride offers, drivers, and customer accounts."

    def handle(self, *args, **options):
        self.stdout.write("Seeding database for BlaBlaCar Mobility app...")

        # 1. Create Demo Customer
        customer, created = User.objects.get_or_create(
            username="customer",
            defaults={
                "email": "customer@aura.com",
                "first_name": "Aarav",
                "last_name": "Sharma",
                "phone": "+919876543210",
                "role": User.Role.CUSTOMER
            }
        )
        if created:
            customer.set_password("pass123")
            customer.save()
            CustomerProfile.objects.get_or_create(user=customer)
            self.stdout.write(self.style.SUCCESS("Created demo customer: customer@aura.com / pass123"))

        # 2. Create Demo Driver & Additional Drivers
        driver_users_data = [
            ("driver", "driver@aura.com", "Rajesh", "Kumar", "+919812345678", "Honda City", "DL-01-AB-1234", "SEDAN"),
            ("driver_vikram", "vikram@aura.com", "Vikram", "Singh", "+919823456789", "Toyota Innova Crysta", "DL-02-CD-5678", "SUV"),
            ("driver_priya", "priya@aura.com", "Priya", "Verma", "+919834567890", "Mercedes E-Class", "DL-03-EF-9012", "PREMIUM")
        ]

        driver_profiles = []
        for uname, email, fname, lname, phone, vehicle_model, vehicle_num, cat in driver_users_data:
            user, u_created = User.objects.get_or_create(
                username=uname,
                defaults={
                    "email": email,
                    "first_name": fname,
                    "last_name": lname,
                    "phone": phone,
                    "role": User.Role.DRIVER
                }
            )
            if u_created:
                user.set_password("pass123")
                user.save()

            dp, _ = DriverProfile.objects.get_or_create(
                user=user,
                defaults={
                    "license_number": f"LIC-{user.id:06d}",
                    "is_online": True,
                    "verification_status": DriverProfile.VerificationStatus.VERIFIED,
                    "rating": 4.90
                }
            )

            driver_profiles.append((user, dp, vehicle_model, vehicle_num, cat))

        self.stdout.write(self.style.SUCCESS(f"Created {len(driver_profiles)} verified drivers."))

        # 3. Create Admin User
        admin, a_created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@aura.com",
                "first_name": "System",
                "last_name": "Admin",
                "phone": "+919999999999",
                "role": User.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True
            }
        )
        if a_created:
            admin.set_password("pass123")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin@aura.com / pass123"))

        # 4. Create Published Carpool Ride Offers (BlaBlaCar Model)
        now = timezone.now()
        sample_offers = [
            {
                "driver": driver_profiles[0][0],
                "origin_address": "Connaught Place, Inner Circle, New Delhi",
                "origin_latitude": 28.6315,
                "origin_longitude": 77.2167,
                "destination_address": "IGI Airport Terminal 3, New Delhi",
                "destination_latitude": 28.5562,
                "destination_longitude": 77.1000,
                "departure_datetime": now + datetime.timedelta(hours=2),
                "total_seats": 3,
                "available_seats": 2,
                "price_per_seat": 150.00,
                "vehicle_model": "Honda City",
                "vehicle_number": "DL-01-AB-1234",
                "vehicle_category": "SEDAN",
                "description": "AC on, non-smoking vehicle. Heading to airport terminal."
            },
            {
                "driver": driver_profiles[1][0],
                "origin_address": "Connaught Place, New Delhi",
                "origin_latitude": 28.6315,
                "origin_longitude": 77.2167,
                "destination_address": "Cyber City, Building 10, Gurugram",
                "destination_latitude": 28.4950,
                "destination_longitude": 77.0890,
                "departure_datetime": now + datetime.timedelta(hours=4),
                "total_seats": 4,
                "available_seats": 4,
                "price_per_seat": 120.00,
                "vehicle_model": "Toyota Innova Crysta",
                "vehicle_number": "DL-02-CD-5678",
                "vehicle_category": "SUV",
                "description": "Daily commute route to Cyber City office hub."
            },
            {
                "driver": driver_profiles[2][0],
                "origin_address": "New Delhi Railway Station",
                "origin_latitude": 28.6430,
                "origin_longitude": 77.2194,
                "destination_address": "Jaipur City Palace, Rajasthan",
                "destination_latitude": 26.9260,
                "destination_longitude": 75.8235,
                "departure_datetime": now + datetime.timedelta(days=1, hours=1),
                "total_seats": 3,
                "available_seats": 3,
                "price_per_seat": 550.00,
                "vehicle_model": "Mercedes E-Class",
                "vehicle_number": "DL-03-EF-9012",
                "vehicle_category": "PREMIUM",
                "description": "Intercity expressway trip to Jaipur. Fast and comfortable."
            }
        ]

        created_offers = []
        for o_data in sample_offers:
            offer, o_created = RideOffer.objects.get_or_create(
                driver=o_data["driver"],
                origin_address=o_data["origin_address"],
                destination_address=o_data["destination_address"],
                defaults=o_data
            )
            created_offers.append(offer)

        self.stdout.write(self.style.SUCCESS(f"Published {len(created_offers)} carpool ride offers."))

        # 5. Create a Sample Reserved Seat Booking for Demo Customer
        if created_offers:
            offer = created_offers[0]
            booking, b_created = Booking.objects.get_or_create(
                customer=customer,
                ride_offer=offer,
                defaults={
                    "driver": driver_profiles[0][1],
                    "seats_booked": 1,
                    "booking_type": BookingType.CARPOOL,
                    "vehicle_category": offer.vehicle_category,
                    "pickup_address": offer.origin_address,
                    "pickup_latitude": offer.origin_latitude,
                    "pickup_longitude": offer.origin_longitude,
                    "destination_address": offer.destination_address,
                    "destination_latitude": offer.destination_latitude,
                    "destination_longitude": offer.destination_longitude,
                    "estimated_distance": 18.5,
                    "estimated_duration": 35,
                    "estimated_fare": offer.price_per_seat,
                    "final_fare": offer.price_per_seat,
                    "status": BookingStatus.DRIVER_ASSIGNED,
                    "scheduled_at": offer.departure_datetime
                }
            )
            if b_created:
                self.stdout.write(self.style.SUCCESS(f"Created sample carpool seat booking: Ref {booking.booking_reference}"))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))

