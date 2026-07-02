import logging
import unittest

from colorama import Fore

from authorization_token import create_token, get_admin_token
from contacts.service.methods_service import get_contacts
from promotions.service.methods_service import get_coupons
from scenarios.work_with_basket.basket_scenario import (
    buy_from_basket_scenario,
)

from scenarios.work_with_basket.assertions_add_and_buy_from_basket import (
    assert_buy_from_basket_result,
)

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def _resolve_coupon_id(*, admin_headers, jira_request_id, client_email):
    if jira_request_id is None:
        return None

    coupon_response = get_coupons(
        headers=admin_headers,
        raw_response=False,
        jira_request_id=jira_request_id,
        contact_email=client_email,
    )
    coupons = coupon_response["response"]["coupons"]
    if not coupons:
        raise AssertionError(
            "Coupon was not found by "
            f"jiraRequestId={jira_request_id} "
            f"client_email={client_email}"
        )
    return coupons[0]["id"]


def _resolve_contact_id(*, admin_headers, client_email):
    contacts_response = get_contacts(
        email=client_email,
        headers=admin_headers,
        raw_response=False,
    )
    contacts = contacts_response["response"].get("contacts", [])
    if not contacts:
        raise AssertionError(f"Contact was not found by email={client_email}")
    return contacts[0]["id"]


def run_buy_from_basket_scenario(
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
    #    Fore.YELLOW + "\nBuy from basket, inline scenario_data",
    #)

    contact_id = _resolve_contact_id(
        admin_headers=admin_headers,
        client_email=scenario_data["client_email"],
    )

    coupon_id = _resolve_coupon_id(
        admin_headers=admin_headers,
        jira_request_id=scenario_data.get("coupon_jiraRequestId"),
        client_email=scenario_data["client_email"],
    )

    result = buy_from_basket_scenario(
        user_headers=user_headers,
        contact_id=contact_id,
        product_type_id=scenario_data["productTypeId"],
        comment=scenario_data["comment"],
        delivery_type_id=scenario_data["deliveryTypeId"],
        skip_send_2_sd=scenario_data["skipSend2SD"],
        coupon_id=coupon_id,
    )

    assert_buy_from_basket_result(testcase,result,"Созданы заказы:")

    logger.info(
        Fore.GREEN + f"\nOrder created from basket: contactId={contact_id}",
    )
    return result
