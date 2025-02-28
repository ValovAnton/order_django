from rest_framework import serializers

from .models import Order, OrderItem, Dish
from .order_enums import OrderStatus
from .services import OrderService
from .validators import OrderValidator, OrderItemValidator, DishValidator


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ["id", "name", "price"]

    def validate(self, attrs):
        DishValidator.validate(attrs)
        return attrs


class OrderItemSerializer(serializers.ModelSerializer):
    dish = DishSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "dish", "price_at_order_moment"]
        read_only_fields = ["price_at_order_moment"]

    def validate(self, attrs):
        OrderItemValidator.validate(attrs)
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "table_number",
            "total_price",
            "status",
            "created_at",
            "updated_at",
            "order_items",
        ]
        read_only_fields = ["id", "total_price", "created_at", "updated_at"]
        extra_kwargs = {
            "status": {"read_only": True, "required": False},
        }

    def validate(self, attrs):
        OrderValidator.validate(attrs)
        return attrs

    def create(self, validated_data):
        order_items_data = validated_data.pop("order_items")
        table = validated_data.pop("table_number")

        order = OrderService.create_order(table=table, items_data=order_items_data)

        return order

    def update(self, instance, validated_data):
        pk = instance.pk
        order = OrderService.update_order(id=pk, order_data=validated_data)
        return order


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)

    def update(self, instance, validated_data):
        return OrderService.update_order_status(instance, validated_data["status"])
