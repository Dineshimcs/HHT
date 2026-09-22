import math
from django.http import JsonResponse

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS coordinates in kilometers.
    """
    R = 6371.0 # Earth radius in kilometers
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2.0) ** 2)
         
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return round(distance, 2)

def json_response_success(data=None, message="Operation successful", status=200):
    """Return a standard structured JSON success response."""
    return JsonResponse({
        "success": True,
        "message": message,
        "data": data or {}
    }, status=status)

def json_response_error(message="An error occurred", code="BAD_REQUEST", details=None, status=400):
    """Return a standard structured JSON error response."""
    return JsonResponse({
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or {}
        }
    }, status=status)
