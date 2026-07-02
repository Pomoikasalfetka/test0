import logging
import unittest
from datetime import UTC, datetime

from colorama import Fore

from authorization_token import get_admin_token
from cards.service.methods_service import create_card
from cards.service.payload import payload_create_card
import shared_test_data

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


SELECTED_TESTS = [
    "test_create_card_standart",
]

CARD_REASON = "Test: create card"
CARD_TYPE_ID = 2
CARD_SUBTYPE_ID = 2
CARD_NUMBER = "000500"


class Cards_basic_tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = get_admin_token()
        cls.admin_headers = {"Authorization": f"Bearer {token}"}

    def test_create_card_standart(self):
        logger.info(
            Fore.YELLOW + "\nСоздание карты",
        )

        payload = payload_create_card(
            reason=CARD_REASON,
            typeId=CARD_TYPE_ID,
            subTypeId=CARD_SUBTYPE_ID,
            cardNumber=CARD_NUMBER,
        )

        response_json = create_card(
            payload=payload,
            headers=self.admin_headers,
            raw_response=False,
        )

        print(response_json)

        card_info = response_json["response"]["cards"][0]
        card_id = card_info['id']

        actual = {
            "cardNumber": card_info['cardNumber'],
        }

        expected = {
            "cardNumber": CARD_NUMBER,
        }

        self.assertEqual(expected, actual)               

        logger.info(
            Fore.GREEN + f"\nЗапрос на создание карты выполнен: {CARD_NUMBER}",
        )


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_name in SELECTED_TESTS:
        if not hasattr(Cards_basic_tests, test_name):
            raise AttributeError(f"Test '{test_name}' not found in Cards_basic_tests")
        suite.addTest(Cards_basic_tests(test_name))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(load_tests(None, None, None))
