from rest_framework import viewsets

from order.models import Order, Dish
from order.serializers import (
    OrderSerializer,
    DishSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    """Api для работы с Orders"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class DishViewSet(viewsets.ModelViewSet):
    """Api для работы с Dishes"""

    queryset = Dish.objects.all()
    serializer_class = DishSerializer
