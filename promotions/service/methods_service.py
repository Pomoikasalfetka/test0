import requests

from config import TEST_SERVER, TIMEOUT
from response_handler import assert_ok_and_get_json

PROMOTIONS_URL = f"{TEST_SERVER}/api/promotions"
COUPONS_URL = f"{TEST_SERVER}/api/coupons"
COUPONS_AUTO_ACTIVATE_URL = f"{TEST_SERVER}/api/coupons/autoActivate"
COUPONS_AUTO_ACTIVATE_BY_OPERATIONS_URL = (
    f"{TEST_SERVER}/api/coupons/autoActivateByOperations"
)


def create_promotion(payload, headers, raw_response):
    response = requests.post(
        PROMOTIONS_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "create promotion")
    return response


def get_promotion(
    *,
    headers,
    raw_response,
    name: str | None = None,
    author: str | None = None,
    active: int | None = None,
    loyalty_program_id: int | None = None,
    coupon_application_type_id: int | None = None,
    start_date_from: str | None = None,
    start_date_to: str | None = None,
    end_date_from: str | None = None,
    end_date_to: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
):
    params = {}

    if name is not None:
        params["name"] = name
    if author is not None:
        params["author"] = author
    if active is not None:
        params["active"] = active
    if loyalty_program_id is not None:
        params["loyaltyProgramId"] = loyalty_program_id
    if coupon_application_type_id is not None:
        params["couponApplicationTypeId"] = coupon_application_type_id
    if start_date_from is not None:
        params["startDateFrom"] = start_date_from
    if start_date_to is not None:
        params["startDateTo"] = start_date_to
    if end_date_from is not None:
        params["endDateFrom"] = end_date_from
    if end_date_to is not None:
        params["endDateTo"] = end_date_to
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

    if not params:
        raise AssertionError("Pass at least one search param for get_promotion.")

    response = requests.get(
        PROMOTIONS_URL,
        headers=headers,
        params=params,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "get promotion")
    return response


def create_coupons(payload, headers, raw_response):
    response = requests.post(
        COUPONS_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "create coupons")
    return response


def get_coupons(
    *,
    headers,
    raw_response,
    coupon_id: int | None = None,
    promotion_id: int | None = None,
    status_id: int | None = None,
    contact_id: int | None = None,
    author: str | None = None,
    jira_request_id: str | None = None,
    code: str | None = None,
    contact_email: str | None = None,
    created_from: str | None = None,
    created_to: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
):
    params = {}

    if coupon_id is not None:
        params["id"] = coupon_id
    if promotion_id is not None:
        params["promotionId"] = promotion_id
    if status_id is not None:
        params["statusId"] = status_id
    if contact_id is not None:
        params["contactId"] = contact_id
    if author is not None:
        params["author"] = author
    if jira_request_id is not None:
        params["jiraRequestId"] = jira_request_id
    if code is not None:
        params["code"] = code
    if contact_email is not None:
        params["contactEmail"] = contact_email
    if created_from is not None:
        params["createdFrom"] = created_from
    if created_to is not None:
        params["createdTo"] = created_to
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

    if not params:
        raise AssertionError("Pass at least one search param for get_coupons.")

    response = requests.get(
        COUPONS_URL,
        headers=headers,
        params=params,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "get coupons")
    return response


def auto_activate_coupons(payload, headers, raw_response):
    response = requests.post(
        COUPONS_AUTO_ACTIVATE_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(response, "auto activate coupons")
    return response


def auto_activate_coupons_by_operations(headers, raw_response):
    response = requests.post(
        COUPONS_AUTO_ACTIVATE_BY_OPERATIONS_URL,
        headers=headers,
        timeout=TIMEOUT,
    )
    if raw_response is False:
        response = assert_ok_and_get_json(
            response,
            "auto activate coupons by operations",
        )
    return response
