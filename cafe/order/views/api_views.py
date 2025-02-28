from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from order.serializers import (
    OrderSerializer,
    OrderStatusUpdateSerializer,
)
from order.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """Api для работы с Orders"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(methods=["patch"], detail=True)
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            updated_order = OrderSerializer(order)
            return Response(updated_order.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
