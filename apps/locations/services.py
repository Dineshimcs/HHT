from common.utilities import calculate_haversine_distance

class LocationService:
    @staticmethod
    def geocode_address(address_string):
        """Simulated geocoding provider abstraction."""
        return {
            'address': address_string,
            'latitude': 28.6139,
            'longitude': 77.2090
        }

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        return calculate_haversine_distance(lat1, lon1, lat2, lon2)
