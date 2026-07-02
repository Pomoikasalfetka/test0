import logging
import unittest

from colorama import Fore

from db.mysql_client import (
    fetch_all,
    get_card_id_by_email,
    get_contact_id_by_email,
    get_latest_cardsmovement_comment_by_card_id,
)

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def get_card_status_by_card_id(*, card_id: int) -> int:
    rows = fetch_all(
        "SELECT status FROM cards WHERE id = %s LIMIT 1",
        (card_id,),
    )
    if not rows:
        raise AssertionError(f"Card was not found for cardId={card_id}")
    return rows[0]["status"]


def run_check_card_status_scenario(*, scenario_data):
    testcase = unittest.TestCase()

    email = scenario_data["email"]
    expected_status = scenario_data.get("status", 5)
    expected_comment_contains = scenario_data.get("expected_comment_contains")

    contact_id = get_contact_id_by_email(email)
    card_id = get_card_id_by_email(email)
    actual_status = get_card_status_by_card_id(card_id=card_id)

    testcase.assertEqual(actual_status, expected_status)

    actual_comment = get_latest_cardsmovement_comment_by_card_id(card_id=card_id)
    if expected_comment_contains is not None:
        testcase.assertIn(expected_comment_contains, actual_comment)

    logger.info(
        Fore.GREEN
        + f"\nCard status check passed: email={email} contactId={contact_id} "
        + f"cardId={card_id} status={actual_status} comment={actual_comment}",
    )
    return {
        "contactId": contact_id,
        "cardId": card_id,
        "status": actual_status,
        "comment": actual_comment,
    }
