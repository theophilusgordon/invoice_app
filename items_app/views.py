from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from .models import Item
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ItemSerializer,
        responses={201: 'Item created successfully.'}
    )
    def perform_create(self, serializer):
        """
        Create a new item.
        """
        serializer.save()
