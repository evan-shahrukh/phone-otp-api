# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, OTPSerializer
from .utils import send_otp_sms
import random

class UserRegistration(generics.GenericAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        otp = random.randint(100000, 999999)
        serializer.validated_data['otp'] = str(otp)
        user = serializer.save()
        
        send_otp_sms(phone_number, otp)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OTPVerification(generics.GenericAPIView):
    serializer_class = OTPSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        user = User.objects.get(otp=str(otp))
        if user:
            user.is_verified = True
            user.otp = None
            user.save()
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
