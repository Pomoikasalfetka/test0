import logging
import unittest

from colorama import Fore

from authorization_token import get_admin_token
from basket.service.methods_service import add_product_to_basket
from basket.service.payload import payload_add_product_to_basket
import shared_test_data

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


SELECTED_TESTS = [
    "test_add_product_to_basket_standart",
]


class BasketBasicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = get_admin_token()
        cls.admin_headers = {"Authorization": f"Bearer {token}"}

    def test_add_product_to_basket_standart(self):
        logger.info(
            Fore.YELLOW + "\nAdd product to basket",
        )

        product_id = shared_test_data.base_busket_entities["product_id"]
        quantity = shared_test_data.base_busket_entities["quantity"]

        payload = payload_add_product_to_basket(
            productId=product_id,
            quantity=quantity,
        )

        response_json = add_product_to_basket(
            payload=payload,
            headers=self.admin_headers,
            raw_response=False,
        )

        self.assertEqual(
            "Товар успешно добавлен в корзину",
            response_json["response"]["msg"],
        )
        self.assertEqual(
            product_id,
            response_json["response"]["basket"][0]["product"]["id"],
        )

        logger.info(
            Fore.GREEN
            + f"\nProduct added to basket: productId={product_id}, quantity={quantity}",
        )


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_name in SELECTED_TESTS:
        if not hasattr(BasketBasicTests, test_name):
            raise AttributeError(f"Test '{test_name}' not found in BasketBasicTests")
        suite.addTest(BasketBasicTests(test_name))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(load_tests(None, None, None))
