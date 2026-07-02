import requests

from config import TEST_SERVER, TIMEOUT
from response_handler import assert_ok_and_get_json

LP_CLIENT_STATUS_HISTORY_URL = f"{TEST_SERVER}/api/LPClientStatusHistory"


def calculate_LPClientStatusHistory(payload, headers, raw_response):
    # Расчет статуса клиента по contactId на сервисе.
    response = requests.post(
        LP_CLIENT_STATUS_HISTORY_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "calculate client status")
    return response
