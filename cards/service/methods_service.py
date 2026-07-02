import requests

from config import TEST_SERVER, TIMEOUT
from response_handler import assert_ok_and_get_json

URL_CREATE_CARD = f"{TEST_SERVER}/api/cards/"


def create_card(payload, headers, raw_response):
    response = requests.post(
        URL_CREATE_CARD,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "create test card")
    return response


def link_user_and_card(card_id, email_user, headers, raw_response):
    response = requests.put(
        f"{TEST_SERVER}/v2/api/cards/{card_id}",
        headers=headers,
        json={"email": email_user},
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "link user and card")
    return response
