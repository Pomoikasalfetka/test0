import logging
import unittest

from colorama import Fore

from authorization_token import get_admin_token
from db.mysql_client import get_contact_id_by_email
from new_condition.service.methods_service import (
    calculate_LPClientStatusHistory as post_LPClientStatusHistory,
)
from new_condition.service.payload import payload_calculate_client_status
from scenarios.new_condition.client_status_scenario import calculate_LPClientStatusHistory

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_calculate_client_status_scenario(*, scenario_data):
    testcase = unittest.TestCase()
    email = scenario_data["email"]
    expected_status_code = scenario_data.get("expected_status_code")
    expected_error_contains = scenario_data.get("expected_error_contains")

    token = get_admin_token()
    admin_headers = {"Authorization": f"Bearer {token}"}

    if expected_status_code is not None:
        contact_id = get_contact_id_by_email(email)
        payload = payload_calculate_client_status(contactId=contact_id)
        response = post_LPClientStatusHistory(
            payload=payload,
            headers=admin_headers,
            raw_response=True,
        )

        testcase.assertEqual(response.status_code, expected_status_code)
        if expected_error_contains is not None:
            testcase.assertIn(expected_error_contains, response.text)

        logger.info(
            Fore.GREEN
            + f"\nClient status error check passed: email={email} contactId={contact_id} "
            + f"status_code={response.status_code} response={response.text}",
        )
        return {
            "contactId": contact_id,
            "statusCode": response.status_code,
            "responseText": response.text,
        }

    contact_id, status_id, result = calculate_LPClientStatusHistory(
        email=email,
        headers=admin_headers,
    )

    logger.info(
        Fore.GREEN
        + f"\nClient status recalculated: email={email} contactId={contact_id} "
        + f"statusId={status_id}",
    )
    return {
        "contactId": contact_id,
        "statusId": status_id,
        "response": result,
    }
