from rest_framework import serializers
from ..models import Invoice, Item
from .address_serializers import AddressSerializer
from .item_serializers import ItemSerializer

class InvoiceSerializer(serializers.ModelSerializer):
    sender_address = AddressSerializer(required=False)
    client_address = AddressSerializer(required=False)
    items = ItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'description',
            'payment_due',
            'payment_terms',
            'status',
            'items',
            'client_name',
            'client_email',
            'client_address',
            'sender_address',
            'created_at',
            'total',
        ]
        read_only_fields = ['id', 'client_name', 'client_email', 'client_address', 'sender_address', 'created_at', 'total']

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        invoice = Invoice.objects.create(
            **validated_data,
        )

        for item_data in items_data:
            Item.objects.create(invoice=invoice, **item_data)

        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        if items_data:
            instance.items.all().delete()
            for item_data in items_data:
                Item.objects.create(invoice=instance, **item_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
