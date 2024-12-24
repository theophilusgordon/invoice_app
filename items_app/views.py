from rest_framework import viewsets

from .models import Item
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Create a new item.

        Example payload:
        {
            "name": "Service 1",
            "quantity": 2,
            "price": 100
        }
        """
        serializer.save()
