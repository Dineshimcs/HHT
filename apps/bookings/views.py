import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from common.utilities import json_response_success, json_response_error
from pricing.services import PricingService
from .services import BookingService
from .models import Booking

@login_required
def create_booking_view(request):
    if request.method == 'POST':
        pickup_addr = request.POST.get('pickup_address', 'Connaught Place, New Delhi')
        pickup_lat = float(request.POST.get('pickup_latitude', 28.6315))
        pickup_lon = float(request.POST.get('pickup_longitude', 77.2167))
        
        drop_addr = request.POST.get('destination_address', 'IGI Airport Terminal 3, New Delhi')
        drop_lat = float(request.POST.get('destination_latitude', 28.5562))
        drop_lon = float(request.POST.get('destination_longitude', 77.1000))
        
        category = request.POST.get('vehicle_category', 'SEDAN')
        booking_type = request.POST.get('booking_type', 'TAXI')
        
        booking = BookingService.create_booking(
            customer=request.user,
            pickup_addr=pickup_addr,
            pickup_lat=pickup_lat,
            pickup_lon=pickup_lon,
            drop_addr=drop_addr,
            drop_lat=drop_lat,
            drop_lon=drop_lon,
            vehicle_category=category,
            booking_type=booking_type
        )
        return redirect('bookings:detail', booking_id=booking.id)

    return render(request, 'customer/booking_create.html')

@login_required
def booking_detail_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'customer/live_trip.html', {'booking': booking})

@require_POST
def api_fare_estimate(request):
    try:
        data = json.loads(request.body)
        category = data.get('category', 'SEDAN')
        distance = float(data.get('distance_km', 8.5))
        duration = int(data.get('duration_mins', 25))
        fare = PricingService.calculate_fare(category, distance, duration)
        return json_response_success({'estimated_fare': float(fare)}, "Fare estimated")
    except Exception as e:
        return json_response_error(str(e))
