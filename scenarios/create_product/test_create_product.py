import logging
import unittest

from colorama import Fore

from authorization_token import get_admin_token
from products.service.methods_service import get_brand, get_category
from providers.service.methods_service import get_provider
from scenarios.create_product.assertions_create_product import (
    assert_created_product_matches_entities,
)
from scenarios.create_product.create_product_scenario import create_product_type_1_scenario
import shared_test_data

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def _prepare_provider_info(provider_info):
    partner = provider_info.get("partner", {})
    return {
        "id": provider_info["id"],
        "name": provider_info["name"],
        "description": provider_info["description"],
        "partnerId": provider_info.get("partnerId", partner.get("id")),
    }


def _prepare_brand_info(brand_info):
    return {
        "id": brand_info["id"],
        "name": brand_info["name"],
        "description": brand_info["description"],
    }


def _prepare_category_info(category_info):
    return {
        "id": category_info["id"],
        "name": category_info["name"],
        "productTypeId": category_info["productTypeId"],
    }


def run_create_product_scenario(*, scenario_data):
    token = get_admin_token()
    admin_headers = {"Authorization": f"Bearer {token}"}
    testcase = unittest.TestCase()

    #logger.info(
    #    Fore.YELLOW + "\nCreate product, inline scenario_data",
    #)

    product_data = scenario_data

    provider_response = get_provider(
        headers=admin_headers,
        raw_response=False,
        name=product_data["provider_name"],
    )
    providers = provider_response["response"]["providers"]
    if not providers:
        raise AssertionError(
            f"Provider was not found by name={product_data['provider_name']}"
        )

    provider_info = providers[0]
    entities_provider = _prepare_provider_info(provider_info)

    brand_response = get_brand(
        headers=admin_headers,
        raw_response=False,
        name=product_data["brand_name"],
    )
    brands = brand_response["response"]["brands"]
    if not brands:
        raise AssertionError(
            f"Brand was not found by name={product_data['brand_name']}"
        )

    brand_info = brands[0]
    entities_brand = _prepare_brand_info(brand_info)

    category_response = get_category(
        headers=admin_headers,
        raw_response=False,
        name=product_data["category_name"],
        product_type_id=product_data["product_type_id"],
    )
    categories = category_response["response"]["categories"]
    if not categories:
        raise AssertionError(
            "Category was not found by "
            f"name={product_data['category_name']} "
            f"product_type_id={product_data['product_type_id']}"
        )

    category_info = categories[0]
    entities_category = _prepare_category_info(category_info)

    result = create_product_type_1_scenario(
        headers=admin_headers,
        product_type_id=product_data["product_type_id"],
        product_id=product_data["product_id"],
        product_name=product_data["product_name"],
        sale_price=product_data["sale_price"],
        supplier_price=product_data["supplier_price"],
        quantity_in_stock=product_data["quantity_in_stock"],
        active=product_data["active"],
        show_on_land=product_data["show_on_land"],
        description_announce=product_data["description_announce"],
        description_detail=product_data["description_detail"],
        vat=product_data["vat"],
        provider=entities_provider,
        brand=entities_brand,
        category=entities_category,
    )
    assert_created_product_matches_entities(testcase, result)

    logger.info(
        Fore.GREEN
        + f"\nCreated product: {result['product']['productId']} type={result['product']['productTypeId']} price={result['product']['salePrice']}",
    )
    return result
