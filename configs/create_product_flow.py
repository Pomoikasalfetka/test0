import uuid

from configs.common_scenario_runners import SCENARIO_RUNNERS


UNIQUE = uuid.uuid4().hex[:6]

PROVIDER_NAME = f"Base provider {UNIQUE}"
BRAND_NAME = f"Base brand {UNIQUE}"
CATEGORY_NAME = f"Base category type {UNIQUE}"
PRODUCT_ID = f"TEST_PRODUCT_TYPE_{UNIQUE}"
PRODUCT_NAME = f"Test product type {UNIQUE}"


RUN_CONFIGS = [
    {
        "scenario": "create_provider",
        "scenario_data": {
            "partner_id": 1,
            "provider_name": PROVIDER_NAME,
            "provider_description": "Base provider description",
        },
    },
    {
        "scenario": "create_brand",
        "scenario_data": {
            "brand_name": BRAND_NAME,
            "brand_description": "Base brand description",
        },
    },
    {
        "scenario": "create_category",
        "scenario_data": {
            "product_type_id": 1,
            "category_name": CATEGORY_NAME,
        },
    },
    {
        "scenario": "create_product",
        "scenario_data": {
            "provider_name": PROVIDER_NAME,
            "brand_name": BRAND_NAME,
            "category_name": CATEGORY_NAME,
            "product_type_id": 1,
            "product_id": PRODUCT_ID,
            "product_name": PRODUCT_NAME,
            "sale_price": 1100,
            "supplier_price": 1100,
            "quantity_in_stock": "Много",
            "active": 1,
            "show_on_land": 1,
            "description_announce": "Новинка 2030 года",
            "description_detail": "Подробное описание товара",
            "vat": 5,
        },
    },
    {
        "scenario": "add_to_basket",
        "scenario_data": {
            "client_email": "avoid2021@yandex.ru",
            "client_password": "Test2020",
            "product_name": PRODUCT_NAME,
            "quantity": 1,
        },
    },
    {
        "scenario": "buy_from_basket",
        "scenario_data": {
            "client_email": "avoid2021@yandex.ru",
            "client_password": "Test2020",
            "productTypeId": 1,
            "comment": "Buy from basket test order",
            "deliveryTypeId": 1,
            "skipSend2SD": 1,
        },
    },
]