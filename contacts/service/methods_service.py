import requests

from config import TEST_SERVER, TIMEOUT
from response_handler import assert_ok_and_get_json

CONTACTS_URL = f"{TEST_SERVER}/api/contacts"
CONTACTS_V2_URL = f"{TEST_SERVER}/v2/api/contacts"
CONTACTS_RESET_URL = f"{TEST_SERVER}/api/service/contacts/reset"


def create_contact(payload, headers, raw_response):
    response = requests.post(
        CONTACTS_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "create test contact")
    return response


def get_contacts(email, headers, raw_response, **params):
    query_params = {
        "email": email,
        **params,
    }
    response = requests.get(
        CONTACTS_V2_URL,
        headers=headers,
        params=query_params,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "get contacts by filters")
    return response


def reset_contact(payload, headers, raw_response):
    response = requests.patch(
        CONTACTS_RESET_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "reset contact")
    return response
