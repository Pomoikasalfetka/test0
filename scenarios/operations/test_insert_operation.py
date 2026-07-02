import logging
from datetime import datetime

from colorama import Fore

from authorization_token import get_admin_token
from contacts.service.methods_service import get_contacts
from db.mysql_client import execute, fetch_all
import shared_test_data

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
            card_id = contacts[0]["cards"][0]["id"]
        except (KeyError, IndexError, TypeError) as exc:
            raise AssertionError(
                f"Card id was not found in contact by email={card_email}"
            ) from exc
        return card_id

    card_id = scenario_data.get("cardId")
    if card_id is None:
        raise AssertionError("Pass cardId or card_email.")
    return card_id


def _resolve_cancel_op_id(*, scenario_data):
    if "cancelOpId" in scenario_data:
        return scenario_data["cancelOpId"]

    cancel_op_source = scenario_data.get("cancelOpSource")
    if cancel_op_source is None:
        cancel_op_source = scenario_data.get("canceledOperationIds")
    if cancel_op_source is None:
        return None

    if isinstance(cancel_op_source, int):
        return cancel_op_source

    rows = fetch_all(
        "SELECT id FROM operations WHERE source=%s ORDER BY id DESC LIMIT 1",
        (cancel_op_source,),
    )
    if not rows:
        raise AssertionError(
            "Canceled operation was not found by source="
            f"{cancel_op_source}"
        )
    return rows[0]["id"]


def _resolve_source(*, scenario_data):
    source = scenario_data.get("source")
    if source is not None:
        return source
    return f"D_{scenario_data['sourceId']}"


def _resolve_datetime(*, scenario_data, field_name: str):
    value = scenario_data.get(field_name)
    if value is not None:
        return value
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def run_insert_operation_scenario(*, scenario_data):
    token = get_admin_token()
    admin_headers = {"Authorization": f"Bearer {token}"}

    card_id = _resolve_card_id(
        scenario_data=scenario_data,
        admin_headers=admin_headers,
    )
    cancel_op_id = _resolve_cancel_op_id(scenario_data=scenario_data)
    source = _resolve_source(scenario_data=scenario_data)
    date_op = _resolve_datetime(scenario_data=scenario_data, field_name="dateOp")
    date_create = _resolve_datetime(
        scenario_data=scenario_data,
        field_name="dateCreate",
    )
    date_update = _resolve_datetime(
        scenario_data=scenario_data,
        field_name="dateUpdate",
    )

    operation_id = execute(
        """
        INSERT INTO operations (
            operationId,
            cardId,
            clientStatusId,
            amount,
            type,
            typeSourceId,
            sourceId,
            comment,
            source,
            partner,
            reason,
            description,
            dateOp,
            cancelOpId,
            dateCreate,
            dateUpdate
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """,
        (
            scenario_data["operationId"],
            card_id,
            scenario_data["clientStatusId"],
            scenario_data["amount"],
            scenario_data["type"],
            scenario_data["typeSourceId"],
            scenario_data["sourceId"],
            scenario_data.get("comment"),
            source,
            scenario_data["partner"],
            scenario_data["reason"],
            scenario_data["description"],
            date_op,
            cancel_op_id,
            date_create,
            date_update,
        ),
    )

    shared_test_data.last_operation_id = operation_id

    logger.info(
        Fore.GREEN
        + f"\nOperation inserted into DB: id={operation_id} "
        + f"operationId={scenario_data['operationId']} cardId={card_id} "
        + f"source={source} cancelOpId={cancel_op_id}",
    )
    return {
        "id": operation_id,
        "cardId": card_id,
        "source": source,
        "cancelOpId": cancel_op_id,
    }
