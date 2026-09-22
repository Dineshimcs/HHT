from django.test import TestCase
from accounts.models import User
from drivers.models import DriverProfile
from dispatch.services import DispatchService

class DispatchEngineTestCase(TestCase):
    def setUp(self):
        # Create driver 1 (online, nearby, verified)
        user1 = User.objects.create_user(username='driver1', role=User.Role.DRIVER)
        self.driver1 = DriverProfile.objects.create(
            user=user1,
            license_number='LIC-001',
            is_online=True,
            is_busy=False,
            verification_status=DriverProfile.VerificationStatus.VERIFIED,
            current_latitude=28.6320,
            current_longitude=77.2170, # ~0.1 km from pickup
            rating=4.9
        )

        # Create driver 2 (offline, far away)
        user2 = User.objects.create_user(username='driver2', role=User.Role.DRIVER)
        self.driver2 = DriverProfile.objects.create(
            user=user2,
            license_number='LIC-002',
            is_online=False,
            is_busy=False,
            verification_status=DriverProfile.VerificationStatus.VERIFIED,
            current_latitude=28.5000,
            current_longitude=77.0000
        )

    def test_find_eligible_drivers_geofence(self):
        pickup_lat, pickup_lon = 28.6315, 77.2167
        eligible = DispatchService.find_eligible_drivers(pickup_lat, pickup_lon, radius_km=5.0)
        
        self.assertEqual(len(eligible), 1)
        self.assertEqual(eligible[0].id, self.driver1.id)
