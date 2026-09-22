from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.http import require_POST
from common.utilities import json_response_success, json_response_error
from .forms import CustomerRegistrationForm, DriverRegistrationForm
from .models import User

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_driver_role():
            return redirect('drivers:dashboard')
        elif request.user.is_admin_role():
            return redirect('admin_ops:dashboard')
        return redirect('customers:dashboard')

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            if user.is_driver_role():
                return redirect('drivers:dashboard')
            elif user.is_admin_role():
                return redirect('admin_ops:dashboard')
            return redirect('customers:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'accounts/login.html')

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to AURA Mobility.")
            return redirect('customers:dashboard')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register_customer.html', {'form': form})

def register_driver(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            license_num = form.cleaned_data.get('license_number')
            from drivers.models import DriverProfile
            DriverProfile.objects.create(user=user, license_number=license_num)
            login(request, user)
            messages.success(request, "Driver registration submitted! Please upload KYC documents for verification.")
            return redirect('drivers:dashboard')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = DriverRegistrationForm()
    return render(request, 'accounts/register_driver.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('landing')

@require_POST
def api_login(request):
    import json
    try:
        data = json.loads(request.body)
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            login(request, user)
            return json_response_success({'user_id': user.id, 'role': user.role}, "Login successful")
        return json_response_error("Invalid credentials", "UNAUTHORIZED", status=401)
    except Exception as e:
        return json_response_error(str(e), "BAD_REQUEST", status=400)
