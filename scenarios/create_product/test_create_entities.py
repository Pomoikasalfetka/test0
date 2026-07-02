import logging
import unittest

from colorama import Fore

from authorization_token import get_admin_token
from scenarios.create_product.prepare_base_product_entities_scenario import (
    create_brand_entity,
    create_category_entity,
    create_provider_entity,
)

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def _get_admin_headers():
    token = get_admin_token()
    if token is None:
        raise AssertionError("Admin token was not created")
    return {"Authorization": f"Bearer {token}"}


def run_create_provider_scenario(*, scenario_data):
    admin_headers = _get_admin_headers()
    testcase = unittest.TestCase()

    #logger.info(Fore.YELLOW + "\nCreate provider, inline scenario_data")

    provider = create_provider_entity(
        headers=admin_headers,
        partner_id=scenario_data["partner_id"],
        provider_name=scenario_data["provider_name"],
        provider_description=scenario_data["provider_description"],
    )

    testcase.assertGreater(provider["id"], 0)
    testcase.assertEqual(provider["name"], scenario_data["provider_name"])

    logger.info(
        Fore.GREEN + f"\nCreated provider: providerId={provider['id']} provider_name={scenario_data["provider_name"]}",
    )
    return provider


def run_create_brand_scenario(*, scenario_data):
    admin_headers = _get_admin_headers()
    testcase = unittest.TestCase()

    #logger.info(Fore.YELLOW + "\nCreate brand, inline scenario_data")

    brand = create_brand_entity(
        headers=admin_headers,
        brand_name=scenario_data["brand_name"],
        brand_description=scenario_data["brand_description"],
    )

    testcase.assertGreater(brand["id"], 0)
    testcase.assertEqual(brand["name"], scenario_data["brand_name"])

    logger.info(
        Fore.GREEN + f"\nCreated brand: brandId={brand['id']} brand_name={scenario_data["brand_name"]}",
    )
    return brand


def run_create_category_scenario(*, scenario_data):
    admin_headers = _get_admin_headers()
    testcase = unittest.TestCase()

    #logger.info(Fore.YELLOW + "\nCreate category, inline scenario_data")

    category = create_category_entity(
        headers=admin_headers,
        product_type_id=scenario_data["product_type_id"],
        category_name=scenario_data["category_name"],
    )

    testcase.assertGreater(category["id"], 0)
    testcase.assertEqual(category["name"], scenario_data["category_name"])
    testcase.assertEqual(category["productTypeId"], scenario_data["product_type_id"])

    logger.info(
        Fore.GREEN + f"\nCreated category: categoryId={category['id']} category_name={scenario_data["category_name"]}",
    )
    return category
