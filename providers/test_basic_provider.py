import logging
import unittest
from datetime import UTC, datetime
from colorama import Fore, Style, init

from authorization_token import get_admin_token
from providers.service.methods_service import create_provider
from providers.service.payload import payload_create_provider
from providers.test_logic.elastic_data import (
    WATING_RESULT_PROVIDERS,
    get_elastic_loyalaty_partners,
)
import shared_test_data

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


SELECTED_TESTS = [
    "test_check_elastic_and_expected_resut",
    "test_create_provider",
    "test_create_provider_negative",
]

class Providers_basic_tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = get_admin_token()
        cls.admin_headers = {"Authorization": f"Bearer {token}"}
        cls.loyalaty_partners = [
            get_elastic_loyalaty_partners(1),
            get_elastic_loyalaty_partners(4),
            get_elastic_loyalaty_partners(5),
            get_elastic_loyalaty_partners(6),
        ]

    def test_check_elastic_and_expected_resut(self):
        logger.info(
            Fore.YELLOW + "\nПроверка данных loyalty partners из elastic с ожидаемым результатом.",
        ) 
        self.assertEqual(self.loyalaty_partners, WATING_RESULT_PROVIDERS)

        logger.info(
            Fore.GREEN + " \n Корректно , Все партнеры из эластика совпали с ожидаемым результатом WATING_RESULT_PROVIDERS:",
        )        

    def test_create_provider(self):
        logger.info(
            Fore.YELLOW + "\nСоздание поставщиков для валидных партнеров и проверка ответа.",
        )             
        suffix = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
        partner_ids = [1, 4, 5, 6]

        for partner_id in partner_ids:
            description = f"Test provider description {partner_id} {suffix}"
            name = f"Test provider name {partner_id} {suffix}"

            payload = payload_create_provider(
                description=description,
                name=name,
                partnerId=partner_id,
            )

            response_json = create_provider(
                payload=payload,
                headers=self.admin_headers,
                raw_response=False,
            )

            provider = response_json["response"]["providers"][0]
            
            shared_test_data.providers_created.append(provider)

            logger.info(
                Fore.GREEN +  "\nПровайдер создан: name=%s description=%s partner_id=%s",
                provider["name"],
                provider["description"],
                provider["partner"]["id"],
            )            

            actual = {
                "description": provider["description"],
                "name": provider["name"],
                "partnerId": provider["partner"]["id"],
            }

            expected = {
                "description": description,
                "name": name,
                "partnerId": partner_id,
            }

            self.assertEqual(expected, actual)
            

    def test_create_provider_negative(self):
        logger.info(
            Fore.YELLOW + "\nПроверка ошибки при создании поставщика с невалидным partner ID.: %s",
        )   
        #Формируем payload     
        suffix = datetime.now(UTC).strftime("%Y%m%d%H%M%S")

        payload = payload_create_provider(
            description=f"Test provider description -1 {suffix}",
            name=f"Test provider name -1 {suffix}",
            partnerId=-1,
        )
        #ПОпытка создать провайдера
        response = create_provider(
            payload=payload,
            headers=self.admin_headers,
            raw_response=True,
        )
        #Ожидаемый результат
        self.assertEqual(response.status_code, 409)
        self.assertIn(
            "Ошибка при добавлении поставщика. Партнер с ID -1 неизвестен",
            response.text,
        )
        logger.info(
            Fore.GREEN + " \n Корректный ожидаемый результат: %s",
            response.text,
        )


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_name in SELECTED_TESTS:
        if not hasattr(Providers_basic_tests, test_name):
            raise AttributeError(f"Test '{test_name}' not found in Providers_basic_tests")
        suite.addTest(Providers_basic_tests(test_name))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(load_tests(None, None, None))
