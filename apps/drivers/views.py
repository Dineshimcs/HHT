import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from common.permissions import driver_required
from common.utilities import json_response_success, json_response_error
from .models import DriverProfile

@login_required
def dashboard(request):
    profile, _ = DriverProfile.objects.get_or_create(
        user=request.user,
        defaults={'license_number': f"LIC-{request.user.id:06d}"}
    )
    from bookings.models import RideOffer, Booking
    published_rides = RideOffer.objects.filter(driver=request.user).order_by('-created_at')
    assigned_bookings = Booking.objects.filter(driver=profile).exclude(status__startswith='CANCELLED').order_by('-created_at')[:10]

    return render(request, 'driver/dashboard.html', {
        'profile': profile,
        'published_rides': published_rides,
        'assigned_bookings': assigned_bookings
    })


@login_required
@require_POST
def toggle_online(request):
    try:
        data = json.loads(request.body)
        is_online = data.get('is_online', False)
        profile = request.user.driver_profile
        profile.is_online = is_online
        profile.save()
        return json_response_success({'is_online': profile.is_online}, "Status updated")
    except Exception as e:
        return json_response_error(str(e))

@login_required
@require_POST
def update_location(request):
    try:
        data = json.loads(request.body)
        profile = request.user.driver_profile
        profile.current_latitude = float(data.get('latitude'))
        profile.current_longitude = float(data.get('longitude'))
        profile.save()
        return json_response_success({}, "Location updated")
    except Exception as e:
        return json_response_error(str(e))
