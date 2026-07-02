import requests

from config import TEST_SERVER, TIMEOUT
from response_handler import assert_ok_and_get_json

BRANDS_URL = f"{TEST_SERVER}/api/brands"
CATEGORIES_URL = f"{TEST_SERVER}/api/categories"
PRODUCTS_URL = f"{TEST_SERVER}/api/products"


def create_brand(payload, headers, raw_response):
    response = requests.post(
        BRANDS_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "create test brand")
    return response


def get_brand_by_id(brand_id, headers, raw_response):
    response = requests.get(
        f"{BRANDS_URL}/{brand_id}",
        headers=headers,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "get brand by id")
    return response


def get_brand(
    *,
    headers,
    raw_response,
    name: str,
    has_product: int | None = None,
    product_type_id: int | None = None,
):
    params = {
        "name": name,
    }
    if has_product is not None:
        params["hasProduct"] = has_product
    if product_type_id is not None:
        params["productTypeId"] = product_type_id

    response = requests.get(
        BRANDS_URL,
        headers=headers,
        params=params,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "get brand by name")
    return response


def create_category(payload, headers, raw_response):
    response = requests.post(
        CATEGORIES_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "create test category")
    return response


def get_category_by_id(category_id, headers, raw_response):
    response = requests.get(
        f"{CATEGORIES_URL}/{category_id}",
        headers=headers,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "get category by id")
    return response


def get_category(
    *,
    headers,
    raw_response,
    name: str,
    product_type_id: int | None = None,
    has_product: int | None = None,
):
    params = {
        "name": name,
    }
    if product_type_id is not None:
        params["productTypeId"] = product_type_id
    if has_product is not None:
        params["hasProduct"] = has_product

    response = requests.get(
        CATEGORIES_URL,
        headers=headers,
        params=params,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "get category by name")
    return response


def create_product(payload, headers, raw_response):
    response = requests.post(
        PRODUCTS_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "create test product")
    return response


def get_product(
    *,
    headers,
    raw_response,
    name: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    product_id: int | None = None,
    provider_product_id: str | None = None,
    product_type_id: int | None = None,
    brand_id: str | None = None,
    active: int | None = None,
    show_on_land: int | None = None,
    provider_id: int | None = None,
    archive: str | None = None,
    category_id: str | None = None,
    sub_category_id: int | None = None,
):
    params = {}

    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if product_id is not None:
        params["id"] = product_id
    if provider_product_id is not None:
        params["productId"] = provider_product_id
    if product_type_id is not None:
        params["productTypeId"] = product_type_id
    if brand_id is not None:
        params["brandId"] = brand_id
    if active is not None:
        params["active"] = active
    if show_on_land is not None:
        params["showOnLand"] = show_on_land
    if provider_id is not None:
        params["providerId"] = provider_id
    if archive is not None:
        params["archive"] = archive
    if category_id is not None:
        params["categoryId"] = category_id
    if sub_category_id is not None:
        params["subCategoryId"] = sub_category_id
    if name is not None:
        params["name"] = name

    if not params:
        raise AssertionError(
            "Pass at least one search param for get_product."
        )

    response = requests.get(
        PRODUCTS_URL,
        headers=headers,
        params=params,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "get product")
    return response
