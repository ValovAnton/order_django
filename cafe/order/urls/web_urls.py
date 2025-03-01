from django.urls import path

from order.views.web_views import (
    CreateOrderView,
    UpdateOrderStatusView,
    OrdersListView,
    TodayProfitView,
    TodayOrdersListView,
    DeleteOrderView,
    OrderRetrieveView,
    ErrorPageView,
)

urlpatterns = [
    path("orders/create/", CreateOrderView.as_view(), name="create_order"),
    path("orders/today/", TodayOrdersListView.as_view(), name="today_orders"),
    path(
        "orders/retrieve/<int:order_id>/",
        OrderRetrieveView.as_view(),
        name="retrieve_order",
    ),
    path(
        "orders/update/<int:order_id>/",
        UpdateOrderStatusView.as_view(),
        name="update_order_status",
    ),
    path(
        "orders/delete_order/<int:order_id>/",
        DeleteOrderView.as_view(),
        name="delete_order",
    ),
    path("orders/", OrdersListView.as_view(), name="order_list"),
    path("today_profit/", TodayProfitView.as_view(), name="today_profit"),
    path("orders/error_page/", ErrorPageView.as_view(), name="error_page"),
]
