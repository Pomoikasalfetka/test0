import json
import logging
import unittest

from colorama import Fore

from authorization_token import get_admin_token
from db.mysql_client import fetch_all
import shared_test_data
from contacts.service.methods_service import get_contacts
from operations.service.methods_service import create_operation
from operations.service.payload import payload_create_operation

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def _resolve_card_id(*, scenario_data, admin_headers):
    card_email = scenario_data.get("card_email")
    if card_email is not None:
        contacts_response = get_contacts(
            email=card_email,
            headers=admin_headers,
            raw_response=False,
            include="cards",
        )
        contacts = contacts_response["response"].get("contacts", [])
        if not contacts:
            raise AssertionError(f"Contact was not found by email={card_email}")

        try:
            # Берем первую карту у первого найденного контакта.
            card_id = contacts[0]["cards"][0]["id"]
        except (KeyError, IndexError, TypeError) as exc:
            raise AssertionError(
                f"Card id was not found in contact by email={card_email}"
            ) from exc
        return card_id

    card_id = scenario_data.get("cardId")
    if card_id is None:
        raise AssertionError(
            "Pass cardId or card_email."
        )
    return card_id


def _resolve_canceled_operation_ids(*, scenario_data):
    canceled_operation_ids = scenario_data.get("canceledOperationIds")
    if canceled_operation_ids is None:
        return None

    if isinstance(canceled_operation_ids, list):
        return canceled_operation_ids
    if isinstance(canceled_operation_ids, int):
        return [canceled_operation_ids]
    if not isinstance(canceled_operation_ids, str):
        raise AssertionError(
            "canceledOperationIds must be list[int], int, or source name str."
        )

    rows = fetch_all(
        "SELECT id FROM operations WHERE source=%s ORDER BY id DESC LIMIT 1",
        (canceled_operation_ids,),
    )
    if not rows:
        raise AssertionError(
            "Canceled operation was not found by source="
            f"{canceled_operation_ids}"
        )
    return [rows[0]["id"]]


def _extract_operation_id(*, result):
    try:
        return result["response"]["id"]
    except (KeyError, TypeError) as exc:
        raise AssertionError(
            "Operation id was not found in create operation response"
        ) from exc


def _parse_create_operation_response(*, response, payload):
    if response.status_code != 201:
        raise AssertionError(
            "Create operation failed: "
            f"status={response.status_code} "
            f"response={response.text} "
            f"payload={payload}"
        )

    try:
        return response.json()
    except json.JSONDecodeError as exc:
        raise AssertionError(
            "Create operation returned non-JSON response: "
            f"status={response.status_code} "
            f"response={response.text} "
            f"payload={payload}"
        ) from exc


def run_create_operation_scenario(*, scenario_data):
    token = get_admin_token()
    admin_headers = {"Authorization": f"Bearer {token}"}
    testcase = unittest.TestCase()

    #logger.info(
    #    Fore.YELLOW + "\nCreate operation, inline scenario_data",
    #)

    card_id = _resolve_card_id(
        scenario_data=scenario_data,
        admin_headers=admin_headers,
    )

    payload = payload_create_operation(
        operationId=scenario_data["operationId"],
        type=scenario_data["type"],
        clientStatusId=scenario_data["clientStatusId"],
        cardId=card_id,
        description=scenario_data["description"],
        amount=scenario_data["amount"],
        partner=scenario_data["partner"],
        reason=scenario_data["reason"],
        typeSourceId=scenario_data["typeSourceId"],
        sourceId=scenario_data["sourceId"],
        comment=scenario_data.get("comment"),
        dateOp=scenario_data.get("dateOp"),
        canceledOperationIds=_resolve_canceled_operation_ids(
            scenario_data=scenario_data
        ),
    )

    response = create_operation(
        payload=payload,
        headers=admin_headers,
        raw_response=True,
    )

    expected_status_code = scenario_data.get("expected_status_code")
    expected_error_contains = scenario_data.get("expected_error_contains")

    if expected_status_code is not None:
        testcase.assertEqual(response.status_code, expected_status_code)
        if expected_error_contains is not None:
            testcase.assertIn(expected_error_contains, response.text)

        logger.info(
            Fore.GREEN
            + f"\nCreate operation error check passed: cardId={card_id} "
            + f"status_code={response.status_code} response={response.text}",
        )
        return {
            "cardId": card_id,
            "statusCode": response.status_code,
            "responseText": response.text,
        }

    result = _parse_create_operation_response(
        response=response,
        payload=payload,
    )

    operation_id = _extract_operation_id(result=result)
    shared_test_data.last_operation_id = operation_id

    #### ТУТ очевидно проверки не правильные . надо проверять с result    
    testcase.assertEqual(payload["operationId"], scenario_data["operationId"])
    testcase.assertEqual(payload["type"], scenario_data["type"])
    testcase.assertEqual(payload["cardId"], card_id)
    testcase.assertEqual(payload["amount"], scenario_data["amount"])

    logger.info(
        Fore.GREEN
        + f"\nOperation created: id={operation_id} operationId={scenario_data['operationId']} "
        + f"description={scenario_data['description']} cardId={card_id} amount={scenario_data['amount']} "
        + f"typeSourceId={scenario_data['typeSourceId']} sourceId={scenario_data['sourceId']}",
    )
    return result
