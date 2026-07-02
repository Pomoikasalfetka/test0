import logging
import unittest

from colorama import Fore

from authorization_token import get_admin_token
from contacts.service.methods_service import create_contact
from contacts.service.payload import payload_create_contact

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


SELECTED_TESTS = [
    "test_create_contact_standart",
]

EMAIL_CONTACT = "avoid2021@yandex.ru"


class ContactBasicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = get_admin_token()
        cls.admin_headers = {"Authorization": f"Bearer {token}"}

    def test_create_contact_standart(self):
        logger.info(
            Fore.YELLOW + "\nСоздание контакта в базе данных",
        )

        payload = payload_create_contact(
            email=EMAIL_CONTACT,
            balance=100000,
            active=1,
        )

        response_json = create_contact(
            payload=payload,
            headers=self.admin_headers,
            raw_response=False,
        )

        contact_info = response_json["response"]["contact"][0]

        actual = {
            "email": contact_info["email"],
        }

        expected = {
            "email": EMAIL_CONTACT,
        }

        self.assertEqual(expected, actual)

        logger.info(
            Fore.GREEN + f"\nЗапрос на создание контакта выполнен: {EMAIL_CONTACT}",
        )


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_name in SELECTED_TESTS:
        if not hasattr(ContactBasicTests, test_name):
            raise AttributeError(f"Test '{test_name}' not found in ContactBasicTests")
        suite.addTest(ContactBasicTests(test_name))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(load_tests(None, None, None))
