from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Order, OrderItem, Dish


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    readonly_fields = ["price_at_order_moment"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = [
        "id",
        "table_number",
        "total_price",
        "status",
        "created_at",
        "updated_at",
    ]

    def save_formset(self, request, form, formset, change):
        """
        Переопределяем сохранение вложенных форм, чтобы обновить total_price.
        """
        instances = formset.save(commit=False)
        order = form.instance  # Текущий заказ

        # Проверяем, есть ли уже существующие позиции или новые
        if not order.order_items.exists() and not instances:
            raise ValidationError("Заказ должен содержать хотя бы одну позицию.")
        for instance in instances:
            if not instance.order_id:
                instance.order = form.instance
            instance.save()  # Сохраняем каждый OrderItem
        formset.save_m2m()
        form.instance.get_total_price()  # Обновляем общую сумму заказа


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ["dish", "price_at_order_moment", "order"]
