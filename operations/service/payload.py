def payload_create_operation(
    *,
    operationId: int,
    type: str,
    clientStatusId: int,
    cardId: int,
    description: str,
    amount: int | float,
    partner: str,
    reason: str,
    typeSourceId: int,
    sourceId: str,
    comment: str | None = None,
    dateOp: str | None = None,
    canceledOperationIds: list[int] | None = None,
):
    payload = {
        "operationId": operationId,
        "type": type,
        "clientStatusId": clientStatusId,
        "cardId": cardId,
        "description": description,
        "amount": amount,
        "partner": partner,
        "reason": reason,
        "typeSourceId": typeSourceId,
        "sourceId": sourceId,
    }

    if comment is not None:
        payload["comment"] = comment
    if dateOp is not None:
        payload["dateOp"] = dateOp
    if canceledOperationIds is not None:
        payload["canceledOperationIds"] = canceledOperationIds

    return payload
