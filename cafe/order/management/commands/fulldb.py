from django.core.management.base import BaseCommand
from order.models import Order, Dish, OrderItem


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными"

    def handle(self, *args, **kwargs):
        try:
            for i in range(1, 5):
                price = i * 100
                table = i * 10
                dish = Dish.objects.create(name=f"СУП №{i}", price=price)
                order = Order.objects.create(table_number=table)
                OrderItem.objects.create(order=order, dish=dish)

            self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))
        except Exception:
            self.stdout.write(self.style.ERROR("База данных не заполнена!"))
