import logging
import unittest

from colorama import Fore

import shared_test_data
from db.mysql_client import get_contact_id_by_email
from scenarios.new_condition.lp_status_queries import get_active_lp_status_details

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_check_contact_last_add_operation_id_scenario(*, scenario_data):
    testcase = unittest.TestCase()

    email = scenario_data["email"]
    expected_operation_id = shared_test_data.last_operation_id
    if expected_operation_id is None:
        raise AssertionError(
            "shared_test_data.last_operation_id is not set. "
            "Create operation before this check."
        )

    contact_id = get_contact_id_by_email(email)
    lp_status_details = get_active_lp_status_details(contact_id=contact_id)
    actual_last_add_operation_id = lp_status_details["lastAddOperationId"]

    testcase.assertEqual(actual_last_add_operation_id, expected_operation_id)

    logger.info(
        Fore.GREEN
        + f"\nContact lastAddOperationId check passed: email={email} contactId={contact_id} "
        + f"lastAddOperationId={actual_last_add_operation_id}",
    )
    return {
        "contactId": contact_id,
        "lastAddOperationId": actual_last_add_operation_id,
    }
