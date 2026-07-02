from configs.common_scenario_runners import SCENARIO_RUNNERS


RUN_CONFIGS = [
    {
        "scenario": "create_provider",
        "scenario_data": {
            "partner_id": 1,
            "provider_name": "Base provider 2",
            "provider_description": "Base provider description 2",
        },
    },
    {
        "scenario": "create_brand",
        "scenario_data": {
            "brand_name": "Base brand 2",
            "brand_description": "Base brand description 2",
        },
    },
    {
        "scenario": "create_category",
        "scenario_data": {
            "product_type_id": 2,
            "category_name": "Base category type 2",
        },
    },
    {
        "scenario": "create_product",
        "scenario_data": {
            "provider_name": "Base provider 2",
            "brand_name": "Base brand 2",
            "category_name": "Base category type 2",
            "product_type_id": 2,
            "product_id": "TEST_EDUCATION_TYPE_2",
            "product_name": "Test education type 1",
            "sale_price": 1,
            "supplier_price": 1,
            "quantity_in_stock": "Много",
            "active": 1,
            "show_on_land": 1,
            "description_announce": "Обучение 2030 года",
            "description_detail": "Подробное описание товара обучения",
            "vat": 5,
        },
    },
#    {
#        "scenario": "add_to_basket",
#        "scenario_data": {
#            "client_email": "avoid2021@yandex.ru",
#            "client_password": "Test2020",
#            "product_name": "Test education type 1",
#            "quantity": 1000,
#        },
#    },
#    {
#        "scenario": "buy_from_basket",
#        "scenario_data": {
#            "client_email": "avoid2021@yandex.ru",
#            "client_password": "Test2020",
#            "productTypeId": 2,
#            "comment": "Buy education from basket test order",
#            "deliveryTypeId": 1,
#            "skipSend2SD": 1,
#        },
#    },
]
