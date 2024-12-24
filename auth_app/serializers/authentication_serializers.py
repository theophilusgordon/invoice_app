from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from auth_app.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'full_name', 'phone', 'profile_photo_url', 'address']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

