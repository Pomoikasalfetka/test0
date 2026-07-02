import logging
import unittest
from datetime import date, datetime

from colorama import Fore

from db.mysql_client import get_contact_id_by_email
from scenarios.new_condition.lp_status_queries import get_active_lp_status_details

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def _normalize_lock_date(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return datetime.strptime(value, "%Y-%m-%d").date()
    raise AssertionError(f"Unsupported lockDate type: {type(value)}")


def run_check_contact_lock_date_scenario(*, scenario_data):
    testcase = unittest.TestCase()

    email = scenario_data["email"]
    expected_lock_date = _normalize_lock_date(scenario_data.get("lockDate"))

    contact_id = get_contact_id_by_email(email)
    lp_status_details = get_active_lp_status_details(contact_id=contact_id)
    actual_lock_date = _normalize_lock_date(lp_status_details["lockDate"])

    testcase.assertEqual(actual_lock_date, expected_lock_date)

    logger.info(
        Fore.GREEN
        + f"\nContact lockDate check passed: email={email} contactId={contact_id} "
        + f"lockDate={actual_lock_date}",
    )
    return {
        "contactId": contact_id,
        "lockDate": actual_lock_date,
    }
