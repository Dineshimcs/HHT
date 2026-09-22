import json
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from common.utilities import json_response_success, json_response_error
from .services import TripService

@login_required
@require_POST
def api_start_trip(request, booking_id):
    try:
        booking = TripService.start_trip(booking_id)
        return json_response_success({'status': booking.status}, "Trip started")
    except Exception as e:
        return json_response_error(str(e))

@login_required
@require_POST
def api_complete_trip(request, booking_id):
    try:
        booking = TripService.complete_trip(booking_id)
        return json_response_success({'status': booking.status, 'final_fare': float(booking.final_fare)}, "Trip completed")
    except Exception as e:
        return json_response_error(str(e))
