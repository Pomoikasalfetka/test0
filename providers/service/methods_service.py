from config import TIMEOUT, TEST_SERVER
import requests
from response_handler import assert_ok_and_get_json

PROVIDER_URL = f"{TEST_SERVER}/api/providers"


def create_provider(payload, headers, raw_response):
    response = requests.post(
        PROVIDER_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response == False:
        response = assert_ok_and_get_json(
            response,
            "Создаем тестового провайдера",
        )
    return response


def get_provider(
    *,
    headers,
    raw_response,
    name: str | None = None,
    partner_id: int | None = None,
):
    params = {}
    if name is not None:
        params["name"] = name
    if partner_id is not None:
        params["partnerId"] = partner_id

    if not params:
        raise AssertionError(
            "Pass at least one search param: name / partner_id."
        )

    response = requests.get(
        PROVIDER_URL,
        headers=headers,
        params=params,
        timeout=TIMEOUT,
    )
    if raw_response == False:
        response = assert_ok_and_get_json(
            response,
            "Поиск провайдера по name / partnerId",
        )
    return response
