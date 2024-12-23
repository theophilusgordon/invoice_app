from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from invoices.models import Invoice
from .serializers.invoice_serializers import InvoiceSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=InvoiceSerializer,
        responses={201: 'Invoice created successfully.'}
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new invoice.
        """
        user = request.user

        customer_name = user.full_name
        customer_email = user.email
        customer_address = user.address

        request.data.update({
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_address": customer_address,
        })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        request_body=InvoiceSerializer,
        responses={200: 'Invoice updated successfully.'}
    )
    def update(self, request, *args, **kwargs):
        """
        Update an invoice.

        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    @swagger_auto_schema(
        request_body=InvoiceSerializer,
        responses={200: 'Invoice status updated successfully'}
    )
    def change_status(self, request, pk=None):
        """
        Change the status of an invoice.
        Example: Mark as paid or pending.
        """
        """
        Custom action to change the status of an invoice.
        Example: Mark as paid or pending.
        """
        invoice = self.get_object()
        new_status = request.data.get("status")
        if new_status not in ['draft', 'pending', 'paid']:
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        invoice.status = new_status
        invoice.save()
        return Response({"status": f"Invoice marked as {new_status}"})
