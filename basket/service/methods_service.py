import requests

from config import TEST_SERVER, TIMEOUT
from response_handler import assert_ok_and_get_json

BASKETS_URL = f"{TEST_SERVER}/api/baskets"
ORDERS_FROM_BASKET_URL = f"{TEST_SERVER}/api/ordersFromBasket"


def add_product_to_basket(payload, headers, raw_response):
    response = requests.post(
        BASKETS_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "add product to basket")
    return response


def create_order_from_basket(payload, headers, raw_response):
    response = requests.post(
        ORDERS_FROM_BASKET_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "create order from basket")
    return response
