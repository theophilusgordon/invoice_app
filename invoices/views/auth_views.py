from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from invoices.utils.send_reset_password_email import send_reset_password_email
from ..models import User
from ..serializers import RegistrationSerializer, LoginSerializer


class RegistrationView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = RegistrationSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		
		access_token = RefreshToken.for_user(user).access_token
		refresh_token = RefreshToken.for_user(user)
		return Response({"access_token": str(access_token), "refresh_token": str(refresh_token), "user": serializer.data}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
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
				"profile_photo_url": user.profile_photo_url,
			}
			return Response({"access_token": str(access_token), "refresh_token": str(refresh_token), "user": user_data}, status=status.HTTP_200_OK)
		return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
	permission_classes = [AllowAny]
	def post(self, request):
		email = request.data.get('email')
		try:
			user = User.objects.get(email=email)
			uid = urlsafe_base64_encode(force_bytes(user.pk))
			token = password_reset_token.make_token(user)

			reset_url = request.build_absolute_uri(
				reverse('reset-password', kwargs={'uidb64': uid, 'token': token})
			)

			send_reset_password_email(user. email, reset_url)

			return Response({'message': 'Password reset link sent.'}, status=200)
		except User.DoesNotExist:
			return Response({'error': 'Invalid email address.'}, status=400)


class ResetPasswordView(APIView):
	def post(self, request, uidb64, token):
		try:
			uid = urlsafe_base64_decode(uidb64).decode()
			user = User.objects.get(pk=uid)

			if not password_reset_token.check_token(user, token):
				return Response({'error': 'Invalid or expired token.'}, status=HTTP_400_BAD_REQUEST)

			new_password = request.data.get('password')
			if not new_password:
				return Response({'error': 'Password is required.'}, status=HTTP_400_BAD_REQUEST)

			user.set_password(new_password)
			user.save()

			return Response({'message': 'Password has been reset successfully.'}, status=HTTP_200_OK)
		except (User.DoesNotExist, ValueError, TypeError):
			return Response({'error': 'Invalid token or user ID.'}, status=HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
	def post(self, request):
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)

password_reset_token = PasswordResetTokenGenerator()
