from decimal import Decimal
from .models import PricingRule
from vehicles.models import VehicleCategory

class PricingService:
    @staticmethod
    def calculate_fare(category, distance_km, duration_mins, surge_multiplier=1.0):
        """
        Calculate total fare for a trip based on pricing rules.
        """
        rule, _ = PricingRule.objects.get_or_create(
            category=category,
            defaults={
                'base_fare': Decimal('60.00'),
                'per_km_rate': Decimal('14.00'),
                'per_minute_rate': Decimal('2.00'),
                'minimum_fare': Decimal('120.00'),
            }
        )

        dist_charge = Decimal(str(distance_km)) * rule.per_km_rate
        time_charge = Decimal(str(duration_mins)) * rule.per_minute_rate
        gross_fare = (rule.base_fare + dist_charge + time_charge) * Decimal(str(surge_multiplier))

        final_fare = max(gross_fare, rule.minimum_fare)
        return round(final_fare, 2)
