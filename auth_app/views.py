from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import User
from .serializers import RegistrationSerializer, LoginSerializer
from invoices.utils.send_reset_password_email import send_reset_password_email

password_reset_token = PasswordResetTokenGenerator()

class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        access_token = RefreshToken.for_user(user).access_token
        refresh_token = RefreshToken.for_user(user)
        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": user.full_name,
            "phone": user.phone,
            "profile_photo_url": user.profile_photo_url,
            "address": user.address
        }
        return Response(
            {"access_token": str(access_token), "refresh_token": str(refresh_token), "user": user_data},
            status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            access_token = RefreshToken.for_user(user).access_token
            refresh_token = RefreshToken.for_user(user)
            user_data = {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": user.full_name,
                "phone": user.phone,
                "profile_photo_url": user.profile_photo_url,
                "address": user.address
            }
            return Response({"access_token": str(access_token), "refresh_token": str(refresh_token), "user": user_data},
                            status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def forgot_password(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = password_reset_token.make_token(user)

            reset_url = request.build_absolute_uri(
                reverse('reset-password', kwargs={'uidb64': uid, 'token': token})
            )

            send_reset_password_email(user.email, reset_url)

            return Response({'message': 'Password reset link sent.'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email address.'}, status=400)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='reset-password/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)')
    def reset_password(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if not password_reset_token.check_token(user, token):
                return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

            new_password = request.data.get('password')
            if not new_password:
                return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not old_password or not new_password or not confirm_password:
            return Response({'error': 'All fields are required.'}, status=400)

        user = authenticate(username=request.user.username, password=old_password)
        if not user:
            return Response({'error': 'Old password is incorrect.'}, status=400)

        if new_password != confirm_password:
            return Response({'error': 'New passwords do not match.'}, status=400)

        if len(new_password) < 8:
            return Response({'error': 'New password must be at least 8 characters long.'}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully.'}, status=200)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)