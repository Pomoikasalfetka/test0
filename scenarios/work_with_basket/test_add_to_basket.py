import logging
import unittest

from colorama import Fore

from authorization_token import create_token, get_admin_token
from products.service.methods_service import get_product
from scenarios.work_with_basket.assertions_add_and_buy_from_basket import (
    assert_add_from_basket_result,
)
from scenarios.work_with_basket.basket_scenario import (
    add_to_basket_scenario,
)

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def _resolve_product_id(*, admin_headers, product_name: str):
    product_response = get_product(
        headers=admin_headers,
        raw_response=False,
        name=product_name,
    )
    products = product_response["response"]["products"]
    if not products:
        raise AssertionError(f"Product was not found by name={product_name}")
    return products[0]["id"]


def run_add_to_basket_scenario(
    *,
    scenario_data,
):
    admin_token = get_admin_token()
    if admin_token is None:
        raise AssertionError("Admin token was not created")

    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_token = create_token(
        scenario_data["client_email"],
        scenario_data["client_password"],
    )
    if user_token is None:
        raise AssertionError("User token was not created")

    user_headers = {"Authorization": f"Bearer {user_token}"}
    testcase = unittest.TestCase()

    #logger.info(
    #    Fore.YELLOW + "\nAdd product to basket, inline scenario_data",
    #)

    product_id = _resolve_product_id(
        admin_headers=admin_headers,
        product_name=scenario_data["product_name"],
    )
    quantity = scenario_data["quantity"]
    if quantity is None:
        raise AssertionError("Basket quantity is empty.")

    result = add_to_basket_scenario(
        user_headers=user_headers,
        product_id=product_id,
        quantity=quantity,
    )

    assert_add_from_basket_result(testcase,result,"Текущая корзина клиента")

    logger.info(
        Fore.GREEN + f"\nProduct added to basket: productId={product_id} product_name={scenario_data["product_name"]} quantity={quantity}",
    )
    return result
