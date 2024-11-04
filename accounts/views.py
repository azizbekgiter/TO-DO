from django.utils import timezone
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, OTP
from .serializers import UserSerializer, OTPVerificationSerializer, SignInSerializer
import random
import string

from rest_framework.permissions import AllowAny

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User(email=email, username=username)
        user.set_password(password)
        user.save()
        

        otp_code = generate_otp()
        expires_at = timezone.now() + timezone.timedelta(minutes=10)
        OTP.objects.create(user=user, otp_code=otp_code, expires_at=expires_at)

        send_mail(
            'Tasdiqlash kodi',
            f"Sizning tasdiqlash kodingiz: {otp_code}",
            'abdusalimovazizbek151@gmail.com',
            [user.email],
            fail_silently=False,
        )


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            user = User.objects.filter(email=email).first()
            if user:
                otp = OTP.objects.filter(user=user, otp_code=otp_code).first()
                if otp and otp.is_valid():
                    user.is_active = True
                    user.save()
                    otp.delete()

                    send_mail(
                        'OTP tasdiqlangan!',
                        'Sizning OTP kodingiz tasdiqlandi. Sahifaga kirishingiz mumkin.',
                        'abdusalimovazizbek151@gmail.com@gmail.com',
                        [user.email],
                        fail_silently=False,
                    )
                    
                    return Response({'message': 'OTP tasdiqlandi. Foydalanuvchi faollashtirildi.'}, status=status.HTTP_200_OK)
                return Response({'detail': 'Noto‘g‘ri yoki muddati o‘tgan OTP!'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'Foydalanuvchi topilmadi!'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({'detail': 'Noto‘g‘ri email yoki parol!'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
