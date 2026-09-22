from decimal import Decimal
from django.test import TestCase
from pricing.services import PricingService
from vehicles.models import VehicleCategory

class FarePricingTestCase(TestCase):
    def test_sedan_fare_calculation(self):
        # 10 km distance, 20 mins duration
        # Base: 60 + (10 * 14) + (20 * 2) = 60 + 140 + 40 = 240
        fare = PricingService.calculate_fare(VehicleCategory.SEDAN, distance_km=10.0, duration_mins=20)
        self.assertEqual(fare, Decimal('240.00'))

    def test_minimum_fare_enforcement(self):
        # Short 0.5 km ride -> gross 60 + 7 + 2 = 69, minimum fare = 120
        fare = PricingService.calculate_fare(VehicleCategory.SEDAN, distance_km=0.5, duration_mins=1)
        self.assertEqual(fare, Decimal('120.00'))
