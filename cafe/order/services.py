from django.utils import timezone

from .models import Order, OrderItem, Dish
from .order_enums import OrderStatus, ErrorMessage


class OrderService:

    @staticmethod
    def create_order(table: int, items_data: list[dict]) -> Order:
        """Создать заказ с позициями"""
        order = Order.objects.create(table_number=table)
        for dish_data in items_data:
            dish, _ = Dish.objects.get_or_create(
                name=dish_data["name"], price=dish_data["price"]
            )
            OrderItem.objects.create(order=order, dish=dish)
        return order

    @staticmethod
    def update_order(
        id: int, order_data: dict
    ) -> Order:  # на будущее, пока не используется
        """функция обновления заказа(статус, номер стола, блюда. Возвращает обновленный заказ"""
        order = Order.objects.get(pk=id)
        table_number = order_data.pop("table_number", order.table_number)
        order_items = order_data.pop("dishes", [])
        order_status = order_data.pop("status", order.status)
        if order_items:
            order.clear_order()
            for dish_data in order_items:
                dish, _ = Dish.objects.get_or_create(
                    name=dish_data["name"], price=dish_data["price"]
                )
                OrderItem.objects.create(order=order, dish=dish)
        order.table_number = table_number
        order.status = order_status
        order.save()
        return order

    @staticmethod
    def update_order_status(order: Order, status: str) -> Order:
        """Обновить статус заказа"""
        if status in OrderStatus.choices:
            order.status = status
            order.save()
            return order
        raise ValueError(ErrorMessage.INVALID_STATUS)

    @staticmethod
    def delete_order(order: Order) -> None:
        """Удалить заказ"""
        order.delete()

    @staticmethod
    def get_all_orders() -> Order:
        return Order.objects.all()

    @staticmethod
    def get_today_orders(filter_date=None) -> Order:
        """Получить заказы за какой-то день,
        если фильтр None, то фильтр = сегодняшний день"""
        filter_date = filter_date or timezone.now().date()
        return Order.objects.filter(created_at__date=filter_date)
