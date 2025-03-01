from django import forms

from order.models import Order, OrderItem
from order.order_enums import OrderStatus


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        status = forms.ChoiceField(choices=OrderStatus.choices)
        fields = ["status"]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["dish"]
