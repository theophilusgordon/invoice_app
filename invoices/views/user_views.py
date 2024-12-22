from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
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

class LogoutView(APIView):
	def post(self, request):
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)