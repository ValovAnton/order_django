import pytest
from django.test import RequestFactory
from django.urls import reverse

from order.views.web_views import CreateOrderView


@pytest.mark.django_db
def test_create_order_view_get():
    factory = RequestFactory()
    request = factory.get(reverse('create_order'))
    response = CreateOrderView.as_view()(request)

    assert response.status_code == 200
