from rest_framework import serializers

class AddressSerializer(serializers.Serializer):
    street = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    post_code = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=100)
