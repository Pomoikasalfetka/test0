import logging
import unittest

from colorama import Fore

from authorization_token import get_admin_token
from promotions.service.methods_service import auto_activate_coupons_by_operations

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_auto_activate_coupons_by_operations_scenario(*, scenario_data):
    token = get_admin_token()
    admin_headers = {"Authorization": f"Bearer {token}"}
    testcase = unittest.TestCase()

    #logger.info(
    #    Fore.YELLOW + "\nAuto activate coupons by operations, inline scenario_data",
    #)

    result = auto_activate_coupons_by_operations(
        headers=admin_headers,
        raw_response=False,
    )

    testcase.assertIsNotNone(result)

    logger.info(
        Fore.GREEN + "\nAuto activation by operations completed",
    )
    return result
