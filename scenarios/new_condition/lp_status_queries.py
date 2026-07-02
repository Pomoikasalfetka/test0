from db.mysql_client import fetch_all


def get_active_lp_status_id(*, contact_id: int) -> int:
    # Возвращает statusId активной записи (active = 1) из lpstatushistory по contactId.
    rows = fetch_all(
        """
        SELECT statusId
        FROM lpstatushistory
        WHERE contactId = %s AND active = 1
        LIMIT 1
        """,
        (contact_id,),
    )
    if not rows:
        raise AssertionError(
            f"Active lp status history was not found for contactId={contact_id}"
        )
    return rows[0]["statusId"]


def get_active_lp_status_details(*, contact_id: int) -> dict:
    # Возвращает dateOfDemotion, tokenBurnDate, countOps, lockDate, lastAddOperationId
    # активной записи (active = 1) из lpstatushistory по contactId.
    rows = fetch_all(
        """
        SELECT dateOfDemotion, tokenBurnDate, countOps, lockDate , lastAddOperationId
        FROM lpstatushistory
        WHERE contactId = %s AND active = 1
        LIMIT 1
        """,
        (contact_id,),
    )
    if not rows:
        raise AssertionError(
            f"Active lp status history was not found for contactId={contact_id}"
        )
    return rows[0]
