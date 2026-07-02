import logging
import unittest
from datetime import date, datetime

from colorama import Fore
from dateutil.relativedelta import relativedelta

from db.mysql_client import get_contact_id_by_email
from scenarios.new_condition.lp_status_queries import get_active_lp_status_details

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def _normalize_date(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return datetime.strptime(value, "%Y-%m-%d").date()
    raise AssertionError(f"Unsupported dateOfDemotion type: {type(value)}")


def run_check_contact_date_of_demotion_scenario(*, scenario_data):
    testcase = unittest.TestCase()

    email = scenario_data["email"]
    months = scenario_data.get("months")

    contact_id = get_contact_id_by_email(email)
    lp_status_details = get_active_lp_status_details(contact_id=contact_id)
    actual_date_of_demotion = _normalize_date(lp_status_details["dateOfDemotion"])

    if months is None:
        expected_date_of_demotion = None
    else:
        expected_date_of_demotion = date.today() + relativedelta(months=months)

    testcase.assertEqual(actual_date_of_demotion, expected_date_of_demotion)

    logger.info(
        Fore.GREEN
        + f"\nContact dateOfDemotion check passed: email={email} contactId={contact_id} "
        + f"dateOfDemotion={actual_date_of_demotion}",
    )
    return {
        "contactId": contact_id,
        "dateOfDemotion": actual_date_of_demotion,
    }
