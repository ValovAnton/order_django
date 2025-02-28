from django.db import models
from enum import Enum


class OrderStatus(models.TextChoices):
    PENDING = "Pending", "В ожидании"
    COMPLETED = "Completed", "Готов"
    CANCELLED = "Cancelled", "Отменен"
    PAID = "Paid", "Оплачен"


class ErrorMessage(Enum):
    MISSING_ORDER_ITEM = "Заказ должен содержать хотя бы один элемент"
    MISSING_DISH = "Заказ должен содержать хотя бы одно блюдо"
    INVALID_STATUS = "Неверный статус заказа"
