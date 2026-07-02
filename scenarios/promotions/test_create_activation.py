import logging
import unittest

from colorama import Fore

from authorization_token import get_admin_token
from promotions.service.methods_service import auto_activate_coupons

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_create_activation_coupon(*, scenario_data):
    token = get_admin_token()
    admin_headers = {"Authorization": f"Bearer {token}"}
    testcase = unittest.TestCase()

    #logger.info(
    #    Fore.YELLOW + "\nActivate coupon, inline scenario_data",
    #)

    payload = scenario_data.get("payload", {})

    result = auto_activate_coupons(
        payload=payload,
        headers=admin_headers,
        raw_response=False,
    )

    testcase.assertIsNotNone(result)

    logger.info(
        Fore.GREEN + "\nCoupon activation completed",
    )
    return result
