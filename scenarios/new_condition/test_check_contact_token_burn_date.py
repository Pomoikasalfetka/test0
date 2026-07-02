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
    raise AssertionError(f"Unsupported tokenBurnDate type: {type(value)}")


def run_check_contact_token_burn_date_scenario(*, scenario_data):
    testcase = unittest.TestCase()

    email = scenario_data["email"]
    months = scenario_data.get("months")

    contact_id = get_contact_id_by_email(email)
    lp_status_details = get_active_lp_status_details(contact_id=contact_id)
    actual_token_burn_date = _normalize_date(lp_status_details["tokenBurnDate"])

    if months is None:
        expected_token_burn_date = None
    else:
        expected_token_burn_date = date.today() + relativedelta(months=months)

    testcase.assertEqual(actual_token_burn_date, expected_token_burn_date)

    logger.info(
        Fore.GREEN
        + f"\nContact tokenBurnDate check passed: email={email} contactId={contact_id} "
        + f"tokenBurnDate={actual_token_burn_date}",
    )
    return {
        "contactId": contact_id,
        "tokenBurnDate": actual_token_burn_date,
    }
