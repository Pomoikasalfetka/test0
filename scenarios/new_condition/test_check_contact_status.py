import logging
import unittest

from colorama import Fore

from db.mysql_client import get_contact_id_by_email
from scenarios.new_condition.lp_status_queries import get_active_lp_status_id

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_check_contact_status_scenario(*, scenario_data):
    testcase = unittest.TestCase()

    email = scenario_data["email"]
    expected_status_id = scenario_data["statusId"]

    contact_id = get_contact_id_by_email(email)
    actual_status_id = get_active_lp_status_id(contact_id=contact_id)

    testcase.assertEqual(actual_status_id, expected_status_id)

    logger.info(
        Fore.GREEN
        + f"\nContact status check passed: email={email} contactId={contact_id} "
        + f"statusId={actual_status_id}",
    )
    return {
        "contactId": contact_id,
        "statusId": actual_status_id,
    }
