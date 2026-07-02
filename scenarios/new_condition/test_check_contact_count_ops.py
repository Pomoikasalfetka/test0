import logging
import unittest

from colorama import Fore

from db.mysql_client import get_contact_id_by_email
from scenarios.new_condition.lp_status_queries import get_active_lp_status_details

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_check_contact_count_ops_scenario(*, scenario_data):
    testcase = unittest.TestCase()

    email = scenario_data["email"]
    expected_count_ops = scenario_data["countOps"]

    contact_id = get_contact_id_by_email(email)
    lp_status_details = get_active_lp_status_details(contact_id=contact_id)
    actual_count_ops = lp_status_details["countOps"]

    testcase.assertEqual(actual_count_ops, expected_count_ops)

    logger.info(
        Fore.GREEN
        + f"\nContact countOps check passed: email={email} contactId={contact_id} "
        + f"countOps={actual_count_ops}",
    )
    return {
        "contactId": contact_id,
        "countOps": actual_count_ops,
    }
