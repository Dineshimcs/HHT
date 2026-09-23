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

    from .models import RideOffer, RideOfferStatus
    open_offers = RideOffer.objects.filter(status=RideOfferStatus.OPEN, available_seats__gt=0).order_by('-departure_datetime')[:10]
    return render(request, 'customer/booking_create.html', {'open_offers': open_offers})

@login_required
def offer_ride_view(request):
    if request.method == 'POST':
        from django.utils import timezone
        import datetime
        origin_addr = request.POST.get('origin_address', 'Connaught Place, New Delhi')
        origin_lat = float(request.POST.get('origin_latitude', 28.6315))
        origin_lon = float(request.POST.get('origin_longitude', 77.2167))
        
        destination_addr = request.POST.get('destination_address', 'IGI Airport Terminal 3, New Delhi')
        destination_lat = float(request.POST.get('destination_latitude', 28.5562))
        destination_lon = float(request.POST.get('destination_longitude', 77.1000))
        
        total_seats = int(request.POST.get('total_seats', 3))
        price_per_seat = float(request.POST.get('price_per_seat', 150.00))
        vehicle_model = request.POST.get('vehicle_model', 'Honda City')
        vehicle_number = request.POST.get('vehicle_number', 'DL-01-AB-1234')
        vehicle_category = request.POST.get('vehicle_category', 'SEDAN')
        description = request.POST.get('description', 'Comfortable ride')
        
        dept_time_str = request.POST.get('departure_time')
        if dept_time_str:
            try:
                departure_dt = timezone.datetime.fromisoformat(dept_time_str)
            except Exception:
                departure_dt = timezone.now() + datetime.timedelta(hours=2)
        else:
            departure_dt = timezone.now() + datetime.timedelta(hours=2)

        offer = BookingService.publish_ride_offer(
            driver=request.user,
            origin_addr=origin_addr,
            origin_lat=origin_lat,
            origin_lon=origin_lon,
            drop_addr=destination_addr,
            drop_lat=destination_lat,
            drop_lon=destination_lon,
            departure_datetime=departure_dt,
            total_seats=total_seats,
            price_per_seat=price_per_seat,
            vehicle_model=vehicle_model,
            vehicle_number=vehicle_number,
            vehicle_category=vehicle_category,
            description=description
        )
        from django.contrib import messages
        messages.success(request, "Your carpool ride offer has been published successfully!")
        return redirect('drivers:dashboard')

    return render(request, 'driver/offer_ride.html')

@login_required
@require_POST
def book_carpool_seat_view(request, offer_id):
    try:
        seats_booked = int(request.POST.get('seats_booked', 1))
        booking = BookingService.book_seat_in_offer(offer_id, request.user, seats_booked)
        from django.contrib import messages
        messages.success(request, f"Seat booked! You reserved {seats_booked} seat(s).")
        return redirect('bookings:detail', booking_id=booking.id)
    except Exception as e:
        from django.contrib import messages
        messages.error(request, f"Could not book seat: {str(e)}")
        return redirect('bookings:create')

@login_required
@require_POST
def cancel_booking_view(request, booking_id):
    try:
        reason = request.POST.get('reason', 'User cancelled from live tracking')
        BookingService.cancel_booking(booking_id, request.user, reason)
        from django.contrib import messages
        messages.info(request, "Trip cancelled successfully.")
        return redirect('customers:dashboard')
    except Exception as e:
        from django.contrib import messages
        messages.error(request, str(e))
        return redirect('bookings:detail', booking_id=booking_id)

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

