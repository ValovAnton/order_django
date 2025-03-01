from datetime import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView

from order.forms import OrderForm
from order.models import Order, Dish
from order.order_enums import OrderStatus
from order.services import OrderService


class CreateOrderView(View):
    def get(self, request):
        dishes = Dish.objects.all()
        return render(request, "orders/create_order.html", {"dishes": dishes})

    def post(self, request):
        table_number = request.POST.get("table_number")
        items_data = []

        names = request.POST.getlist("order_items[][name]")
        prices = request.POST.getlist("order_items[][price]")

        if prices != [""] and names != [""]:  # TODO тут подумай
            if len(prices) == len(names):
                for name, price in zip(names, prices):
                    items_data.append({"name": name, "price": price})

                OrderService.create_order(table_number, items_data)
            return redirect("order_list")
        else:

            return redirect("error_page")


class OrderRetrieveView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        form = OrderForm(instance=order)
        dishes = Dish.objects.all()

        return render(
            request,
            "orders/retrieve.html",
            {
                "form": form,
                "order": order,
                "dishes": dishes,
                "order_status_choices": OrderStatus.choices,
            },
        )


class UpdateOrderStatusView(View):

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        form = OrderForm(instance=order)
        return render(
            request,
            "orders/update_status.html",
            {"form": form, "order": order},
        )

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("order_list")
        else:
            return redirect("error_page")


class BaseOrderListView(ListView):
    """Базовый класс для списка заказов с поиском"""

    model = Order
    template_name = "orders/list_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip().lower().capitalize()
        orders = self.get_orders()
        if query:

            status_map = {
                choice[1]: choice[0] for choice in OrderStatus.choices
            }  # TODO подумай, вынести куда
            status_value = status_map.get(query, query)

            orders = orders.filter(
                Q(table_number__icontains=query) | Q(status__icontains=status_value)
            )

        return orders

    def get_orders(self):
        """ПЕРЕОПРЕДЕЛИ"""
        return Order.objects.none()


class OrdersListView(BaseOrderListView):
    """Класс для отображения всех заказов"""

    def get_orders(self):
        return OrderService.get_all_orders()


class TodayOrdersListView(BaseOrderListView):
    """Класс для отображения сегодняшних заказов"""

    def get_orders(self):
        return OrderService.get_today_orders()


class DeleteOrderView(View):
    """класс для удаления заказа"""

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        OrderService.delete_order(order)
        return redirect("order_list")


class TodayProfitView(TemplateView):
    """класс для подсчета суммы за сегодня"""

    template_name = "orders/today_profit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_param = self.request.GET.get("date", None)

        if date_param:
            "если передали дату, то пробуем, если неверный формат или нет, то сегодня"
            try:
                selected_date = datetime.strptime(date_param, "%Y-%m-%d").date()
            except ValueError:
                selected_date = (
                    timezone.now().date()
                )  # Если формат некорректен, ставим сегодня
        else:
            selected_date = timezone.now().date()

        orders = OrderService.get_today_orders(selected_date).filter(
            status=OrderStatus.COMPLETED
        )

        context["profit"] = sum(order.total_price for order in orders) if orders else 0
        context["date"] = selected_date
        context["today"] = timezone.now().date()
        return context


class ErrorPageView(TemplateView):
    """СТраница error_page"""

    template_name = "orders/error_page.html"
