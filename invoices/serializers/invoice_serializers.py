from rest_framework import serializers
from ..models import Invoice, Item
from .address_serializers import AddressSerializer
from .item_serializers import ItemSerializer

class InvoiceSerializer(serializers.ModelSerializer):
    sender_address = AddressSerializer()
    client_address = AddressSerializer()
    items = ItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'created_at',
            'payment_due',
            'description',
            'payment_terms',
            'client_name',
            'client_email',
            'status',
            'sender_address',
            'client_address',
            'items',
            'total',
        ]

    def create(self, validated_data):
        sender_address_data = validated_data.pop('sender_address')
        client_address_data = validated_data.pop('client_address')
        items_data = validated_data.pop('items')

        invoice = Invoice.objects.create(
            **validated_data,
            sender_address=sender_address_data,
            client_address=client_address_data
        )

        for item_data in items_data:
            Item.objects.create(invoice=invoice, **item_data)

        return invoice

    def update(self, instance, validated_data):
        sender_address_data = validated_data.pop('sender_address', None)
        client_address_data = validated_data.pop('client_address', None)
        items_data = validated_data.pop('items', None)

        if sender_address_data:
            for attr, value in sender_address_data.items():
                setattr(instance.sender_address, attr, value)

        if client_address_data:
            for attr, value in client_address_data.items():
                setattr(instance.client_address, attr, value)

        if items_data:
            instance.items.all().delete()
            for item_data in items_data:
                Item.objects.create(invoice=instance, **item_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
