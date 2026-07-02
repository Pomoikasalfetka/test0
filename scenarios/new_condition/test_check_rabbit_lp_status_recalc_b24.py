import logging
import unittest

from colorama import Fore

from config import RABBIT_SERVER_QUEUE_05
from db.mysql_client import get_card_id_by_email, get_contact_id_by_email
from rabbit.rabbit_client import find_lp_status_recalc_b24_message

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_check_rabbit_lp_status_recalc_b24_scenario(*, scenario_data):
    testcase = unittest.TestCase()

    email = scenario_data["email"]
    contact_id = scenario_data.get("contact_id") or get_contact_id_by_email(email)
    card_id = scenario_data.get("card_id") or get_card_id_by_email(email)
    expect_message = scenario_data.get("expect_message", True)
    queue = scenario_data.get("queue", RABBIT_SERVER_QUEUE_05)
    event_name = scenario_data.get("event_name", "LP_STATUS_RECALC_B24")
    timeout_seconds = scenario_data.get("timeout_seconds", 10)
    delete_on_read = scenario_data.get("delete_on_read", True)

    message = find_lp_status_recalc_b24_message(
        contact_id=contact_id,
        card_id=card_id,
        queue=queue,
        event_name=event_name,
        timeout_seconds=timeout_seconds,
        delete_on_read=delete_on_read,
    )

    if expect_message:
        testcase.assertIsNotNone(
            message,
            f"Message {event_name} for contactId={contact_id} cardId={card_id} "
            f"was not found in queue={queue}",
        )
        testcase.assertEqual(message["event_name"], event_name)
        testcase.assertIn("contactId", message["data"])
        testcase.assertIn("cardId", message["data"])
        testcase.assertEqual(int(message["data"]["contactId"]), int(contact_id))
        testcase.assertEqual(int(message["data"]["cardId"]), int(card_id))

        logger.info(
            Fore.GREEN
            + f"\nRabbit message check passed: queue={queue} event={event_name} "
            + f"contactId={contact_id} cardId={card_id} message={message}",
        )
    else:
        testcase.assertIsNone(
            message,
            f"Unexpected {event_name} message for contactId={contact_id} cardId={card_id} "
            f"in queue={queue}: {message}",
        )
        logger.info(
            Fore.GREEN
            + f"\nRabbit message absence check passed: queue={queue} event={event_name} "
            + f"contactId={contact_id} cardId={card_id}",
        )

    return {
        "contactId": contact_id,
        "cardId": card_id,
        "queue": queue,
        "eventName": event_name,
        "expectMessage": expect_message,
        "message": message,
    }
