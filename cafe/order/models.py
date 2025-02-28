from django.core.exceptions import ValidationError
from django.db import models

from .order_enums import OrderStatus
from .validators import DishValidator, OrderValidator


class Order(models.Model):
    """Модель заказа
    created_at - дата и время создания заказа
    updated_at - дата и время изменения заказа
    table_number - номер стола
    status - статус заказа(см ENUM)
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    table_number = models.PositiveIntegerField(
        verbose_name="Номер стола", validators=[OrderValidator.validate_table]
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name="Статус заказа",
    )

    @property
    def total_price(self):
        return self.get_total_price()

    def __str__(self):
        return f"Заказ № {self.id}, стол: {self.table_number}, сумма: {self.total_price}, статус: {self.status}"

    def clean(self):
        if (
            self.pk and not self.order_items.exists()
        ):  # Если заказ уже существует и не имеет позиций
            raise ValidationError("Заказ должен содержать хотя бы одну позицию.")

    def get_total_price(self):
        try:
            return sum(item.price_at_order_moment for item in self.order_items.all())
        except OrderItem.DoesNotExist:
            return 0

    def clear_order(self):
        self.order_items.all().delete()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]


class OrderItem(models.Model):
    """Промежуточная таблица, связывающая заказ с блюдами и количеством
    order - ссылка на заказ
    dish - ссылка на блюдо
    price_at_order_moment - цена блюда в момент создания заказа
    """

    order = models.ForeignKey(
        Order,
        related_name="order_items",
        on_delete=models.CASCADE,
        verbose_name="Заказ",
    )
    dish = models.ForeignKey("Dish", on_delete=models.CASCADE, verbose_name="Блюдо")
    price_at_order_moment = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )

    def save(self, *args, **kwargs):
        self.price_at_order_moment = self.dish.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dish.name} по цене {self.price_at_order_moment}"

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Заказанные блюда"


class Dish(models.Model):
    """Модель блюда
    name - название блюда
    price - цена блюда
    """

    name = models.CharField(max_length=100, blank=False, verbose_name="Название")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        verbose_name="Цена",
        validators=[DishValidator.validate_price],
    )

    def __str__(self):
        return f"{self.name} : {self.price}"

    class Meta:
        ordering = ["name"]
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
