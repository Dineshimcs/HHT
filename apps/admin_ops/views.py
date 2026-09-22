from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from common.permissions import admin_required
from bookings.models import Booking
from drivers.models import DriverProfile

@login_required
def dashboard(request):
    total_bookings = Booking.objects.count()
    active_trips = Booking.objects.filter(status__in=['TRIP_STARTED', 'TRIP_IN_PROGRESS', 'DRIVER_ASSIGNED']).count()
    available_drivers = DriverProfile.objects.filter(is_online=True, is_busy=False).count()
    recent_bookings = Booking.objects.select_related('customer', 'driver').order_by('-created_at')[:10]

    return render(request, 'admin/dashboard.html', {
        'total_bookings': total_bookings,
        'active_trips': active_trips,
        'available_drivers': available_drivers,
        'recent_bookings': recent_bookings
    })

@login_required
def drivers_list(request):
    drivers = DriverProfile.objects.select_related('user').order_by('-created_at')
    return render(request, 'admin/drivers.html', {'drivers': drivers})

@login_required
def verify_driver(request, driver_id):
    driver = get_object_or_404(DriverProfile, id=driver_id)
    driver.verification_status = DriverProfile.VerificationStatus.VERIFIED
    driver.save()
    messages.success(request, f"Driver {driver.user.get_full_name() or driver.user.username} has been verified.")
    return redirect('admin_ops:drivers')
