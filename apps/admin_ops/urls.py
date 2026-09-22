from django.urls import path
from . import views

app_name = 'admin_ops'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('drivers/', views.drivers_list, name='drivers'),
    path('drivers/<int:driver_id>/verify/', views.verify_driver, name='verify_driver'),
]
