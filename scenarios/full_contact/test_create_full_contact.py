import logging
import unittest

from colorama import Fore

import shared_test_data
from authorization_token import get_admin_token
from scenarios.full_contact.assertions_full_contact import assert_created_full_contact
from scenarios.full_contact.contact_card_scenario import create_full_contact

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_full_contact_scenario(*, scenario_data):
    token = get_admin_token()
    admin_headers = {"Authorization": f"Bearer {token}"}
    testcase = unittest.TestCase()

    full_contact_data = scenario_data

    #logger.info(
    #    Fore.YELLOW
    #    + f"\nСоздание контакта, email={full_contact_data['email']}",
    #)

    result = create_full_contact(
        headers=admin_headers,
        email=full_contact_data["email"],
        card_number=full_contact_data["card_number"],
        type_id=full_contact_data["card_type_id"],
        subtype_id=full_contact_data["card_subtype_id"],
        reason=full_contact_data["card_reason"],
        balance=full_contact_data["balance"],
    )
    shared_test_data.contacts_with_cards.append(result)

    assert_created_full_contact(testcase, result, full_contact_data)

    logger.info(
        Fore.GREEN
        + f"\nСценарий Создание контакта выполнен: "
        + f"{result['contact']['email']} ({result['card']['cardNumber']}) Баланс: {result['contact']["balance"]}",
    )
    return result
