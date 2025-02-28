import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Order
from ..order_enums import OrderStatus

#

#
# @pytest.mark.django_db
# class TestOrderApi:
#     def test_create_order():
#         client = APIClient()
#         response = client.post("/api/orders/", {"table_number": 5})
#         assert response.status_code == 201
#

# @pytest.mark.django_db
# class TestOrderAPI:
#     def setup_method(self):
#         """Создаем тестовый заказ перед каждым тестом"""
#         self.order = Order.objects.create(table_number=5, status=OrderStatus.PENDING)
#         self.order_url = reverse("order-detail", args=[self.order.id])
#         self.update_status_url = reverse("order-update-status", args=[self.order.id])
#
#     def test_get_order_list(self, client):
#         """Тест получения списка заказов"""
#         response = client.get(reverse("order-list"))
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == Order.objects.count()
#
#     def test_get_order_detail(self, client):
#         """Тест получения одного заказа"""
#         response = client.get(self.order_url)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["id"] == self.order.id
#
#     def test_create_order(self, client):
#         """Тест создания заказа"""
#         data = {"table_number": 10, "status": OrderStatus.PENDING}
#         response = client.post(reverse("order-list"), data)
#         assert response.status_code == status.HTTP_201_CREATED
#         assert Order.objects.count() == 2
#
#     def test_update_order(self, client):
#         """Тест обновления заказа"""
#         data = {"table_number": 8}
#         response = client.patch(self.order_url, data)
#         assert response.status_code == status.HTTP_200_OK
#         self.order.refresh_from_db()
#         assert self.order.table_number == 8
#
#     def test_update_order_status(self, client):
#         """Тест обновления статуса заказа через кастомный action"""
#         data = {"status": OrderStatus.COMPLETED}
#         response = client.patch(self.update_status_url, data)
#         assert response.status_code == status.HTTP_200_OK
#         self.order.refresh_from_db()
#         assert self.order.status == OrderStatus.COMPLETED
#
#     def test_delete_order(self, client):
#         """Тест удаления заказа"""
#         response = client.delete(self.order_url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert not Order.objects.filter(id=self.order.id).exists()
