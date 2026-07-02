def payload_create_card(
    *,
    reason: str,
    typeId: int,
    subTypeId: int,
    cardNumber: str,
):
    payload = {
        "reason": reason,
        "cardsInfo": [
            {
                "typeId": typeId,
                "subTypeId": subTypeId,
                "cardNumber": cardNumber,
            }
        ],
    }
    return payload
