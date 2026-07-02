import logging
import unittest

from colorama import Fore

from authorization_token import get_admin_token
from promotions.service.methods_service import create_coupons, get_promotion
from promotions.service.payload import payload_create_coupons

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_create_coupons_scenario(*, scenario_data):
    token = get_admin_token()
    admin_headers = {"Authorization": f"Bearer {token}"}
    testcase = unittest.TestCase()

    #logger.info(
    #    Fore.YELLOW + "\nCreate coupons, inline scenario_data",
    #)

    promotion_response = get_promotion(
        headers=admin_headers,
        raw_response=False,
        name=scenario_data["promotion_name"],
    )
    promotions = promotion_response["response"]["promotions"]
    if not promotions:
        raise AssertionError(
            f"Promotion was not found by name={scenario_data['promotion_name']}"
        )

    promotion = promotions[0]
    payload = payload_create_coupons(
        promotionId=promotion["id"],
        emails=[scenario_data["email"]],
        jiraRequestId=scenario_data["jiraRequestId"],
        comment=scenario_data.get("comment"),
    )

    result = create_coupons(
        payload=payload,
        headers=admin_headers,
        raw_response=False,
    )

    testcase.assertEqual(payload["promotionId"], promotion["id"])
    testcase.assertEqual(payload["emails"], [scenario_data["email"]])
    testcase.assertEqual(payload["jiraRequestId"], scenario_data["jiraRequestId"])

    logger.info(
        Fore.GREEN
        + f"\nCoupons created: promotion={scenario_data['promotion_name']} email={scenario_data['email']}",
    )
    return result
