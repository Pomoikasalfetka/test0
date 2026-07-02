import requests

from config import TEST_SERVER, TIMEOUT
from response_handler import assert_ok_and_get_json

OPERATIONS_URL = f"{TEST_SERVER}/v2/api/operations"


def create_operation(payload, headers, raw_response):
    response = requests.post(
        OPERATIONS_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "create operation")
    return response
