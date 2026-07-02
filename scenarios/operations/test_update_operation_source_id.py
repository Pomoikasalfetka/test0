import logging

from colorama import Fore

from db.mysql_client import execute, fetch_all, get_card_id_by_email

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

UPDATEABLE_FIELDS = {
    "operationId",
    "clientStatusId",
    "amount",
    "type",
    "typeSourceId",
    "sourceId",
    "comment",
    "source",
    "partner",
    "reason",
    "description",
    "dateOp",
    "cancelOpId",
}

def _get_latest_operation_by_card_id(*, card_id: int) -> dict:
    rows = fetch_all(
        """
        SELECT *
        FROM operations
        WHERE cardId = %s
        ORDER BY id DESC
        LIMIT 1
        """,
        (card_id,),
    )
    if not rows:
        raise AssertionError(f"Operation was not found for cardId={card_id}")
    return rows[0]


def _extract_fields_to_update(*, scenario_data) -> dict:
    if "fields" in scenario_data:
        updates = dict(scenario_data["fields"])
    else:
        updates = {
            key: scenario_data[key]
            for key in UPDATEABLE_FIELDS
            if key in scenario_data
        }

    if not updates:
        return {}

    unknown_fields = set(updates) - UPDATEABLE_FIELDS
    if unknown_fields:
        raise AssertionError(
            "Unsupported operation fields: "
            f"{', '.join(sorted(unknown_fields))}"
        )
    return updates


def run_update_operation_source_id_scenario(*, scenario_data):
    card_email = scenario_data["card_email"]
    updates = _extract_fields_to_update(scenario_data=scenario_data)

    card_id = get_card_id_by_email(card_email)
    operation = _get_latest_operation_by_card_id(card_id=card_id)
    operation_id = operation["id"]

    if not updates:
        logger.info(
            Fore.GREEN
            + f"\nOperation update skipped: email={card_email} cardId={card_id} "
            + f"id={operation_id} no fields to update",
        )
        return {
            "cardId": card_id,
            "id": operation_id,
            "updates": {},
        }

    set_clause = ", ".join(f"{field} = %s" for field in updates)
    params = [*updates.values(), operation_id]
    execute(
        f"UPDATE operations SET {set_clause} WHERE id = %s",
        tuple(params),
    )

    changes = ", ".join(
        f"{field}={operation.get(field)!r}->{updates[field]!r}"
        for field in updates
    )
    logger.info(
        Fore.GREEN
        + f"\nOperation updated: email={card_email} cardId={card_id} "
        + f"id={operation_id} {changes}",
    )
    return {
        "cardId": card_id,
        "id": operation_id,
        "oldValues": {field: operation.get(field) for field in updates},
        "updates": updates,
    }
