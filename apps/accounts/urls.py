from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/driver/', views.register_driver, name='register_driver'),
    path('logout/', views.logout_view, name='logout'),
    path('api/login/', views.api_login, name='api_login'),
]
