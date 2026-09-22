from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from common.permissions import customer_required

@login_required
def dashboard(request):
    profile = request.user.customer_profile if hasattr(request.user, 'customer_profile') else (None, None)
    return render(request, 'customer/dashboard.html', {
        'profile': profile
    })

@login_required
def trip_history(request):
    from bookings.models import Booking
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'customer/history.html', {'bookings': bookings})
