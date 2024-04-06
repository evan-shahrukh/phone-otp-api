from django.urls import path
from .views import UserRegistration , OTPVerification

urlpatterns = [
    path('registration/', UserRegistration.as_view() , name="registration"),
    path('verification/', OTPVerification.as_view() , name="verification"),
]
