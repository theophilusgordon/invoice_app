from rest_framework import serializers
from ..models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'quantity', 'price', 'total']
        read_only_fields = ['id', 'total']
