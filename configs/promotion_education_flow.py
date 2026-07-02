from datetime import UTC, datetime, timedelta

from configs.common_scenario_runners import SCENARIO_RUNNERS


PROMOTION_START_DATE = (
    datetime.now(UTC) - timedelta(days=1)
).replace(
    hour=0,
    minute=0,
    second=0,
    microsecond=0,
).strftime("%Y-%m-%dT%H:%M:%SZ")

PROMOTION_END_DATE = (
    datetime.now(UTC) + timedelta(days=365)
).replace(
    hour=23,
    minute=59,
    second=59,
    microsecond=0,
).strftime("%Y-%m-%dT%H:%M:%SZ")


RUN_CONFIGS = [
    {
        "scenario": "create_promotion",
        "scenario_data": {
            "name": "Test promotion from flow for education",
            "description": "Promotion for basket flow for education",
            "startDate": PROMOTION_START_DATE,
            "endDate": PROMOTION_END_DATE,
            "activationConditionId": 1,
            "couponApplicationTypeId": 2,
            "couponName": "FLOW_PROMO",
            "couponNominal": 700,
            "loyaltyProgramId": 1,
            "active": 1,
            "couponValidityDays": None,
            "couponCodeLength": 8,
            "couponCodeCharset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            "couponCodePrefix": "FLOW",
            "comment": "Promotion flow test for education",
        },
    },
    {
        "scenario": "create_coupons",
        "scenario_data": {
            "promotion_name": "Test promotion from flow for education",
            "email": "avoid2021@yandex.ru",
            "jiraRequestId": "PROMO-TEST-100-EDUCATION",
            "comment": "Create coupon for user from flow for education",
        },
    },
    {
        "scenario": "activate_coupon",
        "scenario_data": {},
    },
    {
        "scenario": "auto_activate_coupons_by_operations",
        "scenario_data": {},
    },
    {
        "scenario": "add_to_basket",
        "scenario_data": {
            "client_email": "avoid2021@yandex.ru",
            "client_password": "Test2020",
            "product_name": "Test education type 1",
            "quantity": 700,
        },
    },
    {
        "scenario": "buy_from_basket",
        "scenario_data": {
            "client_email": "avoid2021@yandex.ru",
            "client_password": "Test2020",
            "coupon_jiraRequestId": "PROMO-TEST-100-EDUCATION",
            "productTypeId": 2,
            "comment": "Buy from basket test order - EDUCATION",
            "deliveryTypeId": 1,
            "skipSend2SD": 1,
        },
    },

]
