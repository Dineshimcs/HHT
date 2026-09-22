from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

from django.http import HttpResponse, FileResponse
import os

def landing_page(request):
    return render(request, 'customer/landing.html')

def service_worker(request):
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'sw.js')
    return FileResponse(open(sw_path, 'rb'), content_type='application/javascript')

urlpatterns = [
    path('favicon.ico', lambda request: HttpResponse(status=204)),
    path('sw.js', service_worker, name='service_worker'),
    path('django-admin/', admin.site.urls),
    path('', landing_page, name='landing'),
    
    path('accounts/', include('accounts.urls')),
    path('customer/', include('customers.urls')),
    path('driver/', include('drivers.urls')),
    path('booking/', include('bookings.urls')),
    path('trip/', include('trips.urls')),
    path('admin-ops/', include('admin_ops.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
