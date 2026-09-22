from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/online/', views.toggle_online, name='toggle_online'),
    path('api/location/', views.update_location, name='update_location'),
]
