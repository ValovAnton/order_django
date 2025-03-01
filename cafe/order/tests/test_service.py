import pytest
from django.utils import timezone

from order.models import Order, Dish, OrderItem
from order.order_enums import OrderStatus, ErrorMessage
from order.services import OrderService


@pytest.mark.django_db
class TestOrderService:
    @pytest.fixture
    def sample_dish(self):
        """Фикстура для создания тестового блюда."""
        return Dish.objects.create(name="Суши", price=15.0)

    @pytest.fixture
    def sample_order(self, sample_dish):
        """Фикстура для создания тестового заказа."""
        order = Order.objects.create(table_number=1, status=OrderStatus.PENDING)
        OrderItem.objects.create(order=order, dish=sample_dish)
        return order

    def test_create_order(self):
        """Тест создания заказа."""
        items_data = [{"name": "Пицца", "price": 10.0}, {"name": "Суши", "price": 15.0}]
        order = OrderService.create_order(table=1, status=OrderStatus.PENDING, items_data=items_data)

        assert order.table_number == 1
        assert order.status == OrderStatus.PENDING
        assert order.order_items.count() == 2
        assert Dish.objects.count() == 2

    def test_update_order(self, sample_order, sample_dish):
        """Тест обновления заказа."""
        updated_data = {
            "table_number": 2,
            "status": OrderStatus.COMPLETED,
            "dishes": [{"name": "Пицца", "price": 10.0}]
        }
        updated_order = OrderService.update_order(id=sample_order.id, order_data=updated_data)

        assert updated_order.table_number == 2
        assert updated_order.status == OrderStatus.COMPLETED.value
        assert updated_order.order_items.count() == 1
        assert updated_order.order_items.first().dish.name == "Пицца"

    def test_update_order_status(self, sample_order):
        """Тест обновления статуса заказа."""
        updated_order = OrderService.update_order_status(order=sample_order,
                                                         status=OrderStatus.choices[1])  # OrderStatus.COMPLETED.value)

        assert updated_order.status == OrderStatus.choices[1]

    def test_update_order_status_invalid(self, sample_order):
        """Тест обновления статуса заказа с неверным статусом."""
        with pytest.raises(ValueError) as exc_info:
            OrderService.update_order_status(order=sample_order, status="INVALID_STATUS")

        assert exc_info.value.args[0] == ErrorMessage.INVALID_STATUS

    def test_delete_order(self, sample_order):
        """Тест удаления заказа."""
        OrderService.delete_order(order=sample_order)
        assert Order.objects.count() == 0

    def test_get_all_orders(self, sample_order):
        """Тест получения всех заказов."""
        orders = OrderService.get_all_orders()
        assert orders.count() == 1
        assert orders.first().id == sample_order.id

    def test_get_today_orders(self, sample_order):
        """Тест получения заказов за сегодня."""
        today_orders = OrderService.get_today_orders()
        assert today_orders.count() == 1
        assert today_orders.first().id == sample_order.id

    def test_get_today_orders_with_filter(self, sample_order):
        """Тест получения заказов за определенную дату."""
        filter_date = timezone.now().date()
        today_orders = OrderService.get_today_orders(filter_date=filter_date)
        assert today_orders.count() == 1
        assert today_orders.first().id == sample_order.id
