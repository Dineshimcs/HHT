from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages

def role_required(*roles):
    """
    Decorator for views that checks if the user has one of the specified roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to access this page.")
                return redirect('accounts:login')
            if request.user.role not in roles and not request.user.is_superuser:
                messages.error(request, "You do not have permission to access this page.")
                raise PermissionDenied("User does not have required role access.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def customer_required(view_func):
    return role_required('CUSTOMER')(view_func)

def driver_required(view_func):
    return role_required('DRIVER')(view_func)

def admin_required(view_func):
    return role_required('ADMIN')(view_func)
