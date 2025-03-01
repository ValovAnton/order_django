import json

import pytest


### region TEST API ORDERS
@pytest.mark.django_db
def test_create_order(api_client, get_order_for_post, url_api_order):
    """Тест создания заказа"""
    response = api_client.post(
        url_api_order,
        data=json.dumps(get_order_for_post),
        content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json()["table_number"] == get_order_for_post["table_number"]
    assert len(response.json()["order_items"]) == len(get_order_for_post["dishes"])


@pytest.mark.django_db
def test_create_order_diff_status(api_client, get_order_for_post, url_api_order):
    """Тест создания заказа, c нестандартным статусом"""
    # get_order_for_post = get_order_for_post.copy()
    get_order_for_post["status"] = "Completed"
    response = api_client.post(
        url_api_order,
        data=json.dumps(get_order_for_post),
        content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json()["table_number"] == get_order_for_post["table_number"]
    assert response.json()["status"] == "Completed"
    assert len(response.json()["order_items"]) == len(get_order_for_post["dishes"])


### region Errors tests

@pytest.mark.django_db
def test_error_table_create_order(api_client, get_order_for_post, url_api_order):
    """Тест создания заказа с некорректным номером стола"""
    get_order_for_post["table_number"] = "-1"
    response = api_client.post(
        url_api_order,
        data=json.dumps(get_order_for_post),
        content_type="application/json"
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_error_dishes_create_order(api_client, get_order_for_post, url_api_order):
    """Тест создания заказа с пустым списком блюд"""
    get_order_for_post["dishes"] = []
    response = api_client.post(
        url_api_order,
        data=json.dumps(get_order_for_post),
        content_type="application/json"
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_error_status_create_order(api_client, get_order_for_post, url_api_order):
    """Тест создания заказа с некорректным статусом"""
    get_order_for_post["status"] = "Done"
    response = api_client.post(
        url_api_order,
        data=json.dumps(get_order_for_post),
        content_type="application/json"
    )
    assert response.status_code == 400


### endregion tests

@pytest.mark.django_db
def test_list_orders(api_client, url_api_order, get_order_for_post):
    """Тест получения списка из 2 заказов"""
    api_client.post(url_api_order, data=json.dumps(get_order_for_post), content_type="application/json")
    api_client.post(url_api_order, data=json.dumps(get_order_for_post), content_type="application/json")

    response = api_client.get(url_api_order)
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.django_db
def test_retrieve_order(api_client, url_api_order, get_order_for_post):
    """Тест получения данных 1 заказа"""
    response = api_client.post(url_api_order, data=json.dumps(get_order_for_post), content_type="application/json")
    assert response.status_code == 201
    assert response.json()["id"] > 0
    id = response.json()["id"]

    response = api_client.get(f"{url_api_order}{id}/")
    assert response.status_code == 200
    assert len(response.json()["order_items"]) == len(get_order_for_post["dishes"])


### endregion

### region TEST API DISHES
@pytest.mark.django_db
def test_create_dishes(api_client, get_dish_for_post, url_api_dishes):
    """Тест создания блюда"""
    response = api_client.post(
        url_api_dishes,
        data=json.dumps(get_dish_for_post),
        content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json()["name"] == get_dish_for_post["name"]
    assert response.json()["price"] == get_dish_for_post["price"]


@pytest.mark.django_db
def test_list_dishes(api_client, url_api_dishes, get_dish_for_post):
    """Тест получения списка блюд"""
    api_client.post(url_api_dishes, data=json.dumps(get_dish_for_post), content_type="application/json")
    api_client.post(url_api_dishes, data=json.dumps(get_dish_for_post), content_type="application/json")

    response = api_client.get(url_api_dishes)
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.django_db
def test_retrieve_dish(api_client, url_api_dishes, get_dish_for_post):
    """Тест получения данных 1 блюда"""
    response = api_client.post(url_api_dishes, data=json.dumps(get_dish_for_post), content_type="application/json")
    assert response.status_code == 201
    assert response.json()["id"] > 0
    id = response.json()["id"]

    response = api_client.get(f"{url_api_dishes}{id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_dish(api_client, url_api_dishes, get_dish_for_post):
    """Тест удаления блюда"""
    response = api_client.post(url_api_dishes, data=json.dumps(get_dish_for_post), content_type="application/json")
    assert response.status_code == 201
    assert response.json()["id"] > 0
    id = response.json()["id"]

    response = api_client.delete(f"{url_api_dishes}{id}/")
    assert response.status_code == 204  # No Content


@pytest.mark.django_db
def test_error_name_create_dish(api_client, get_dish_for_post, url_api_dishes):
    """Тест создания блюда с некорректным названием"""
    get_dish_for_post["name"] = ""
    response = api_client.post(
        url_api_dishes,
        data=json.dumps(get_dish_for_post),
        content_type="application/json"
    )
    assert response.status_code == 400


@pytest.mark.django_db
@pytest.mark.parametrize("new_price", [0, -1, "-1", "0", "", "str", None])
def test_error_price_create_dish(api_client, get_dish_for_post, url_api_dishes, new_price):
    """Тест создания блюда с некорректным ценой"""
    get_dish_for_post["price"] = new_price
    response = api_client.post(
        url_api_dishes,
        data=json.dumps(get_dish_for_post),
        content_type="application/json"
    )
    assert response.status_code == 400

### endregion
