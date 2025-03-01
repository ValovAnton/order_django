import pytest
from rest_framework.test import APIClient


### region api Fixtures
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def url_api_order():
    return '/api/v1/orders/'


@pytest.fixture
def get_order_for_post():
    post_data = {
        "table_number": 1,
        "status": "Pending",
        "dishes": [
            {
                "name": "Суши",
                "price": "15.00"
            }
        ]}
    return post_data


@pytest.fixture
def url_api_dishes():
    return '/api/v1/dishes/'


@pytest.fixture
def get_dish_for_post():
    post_data = {
        "name": "Суши",
        "price": "15.15"
    }
    return post_data

### endregion
