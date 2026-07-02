def payload_add_product_to_basket(
    *,
    productId: int = 1559,
    quantity: int = 1,
    contactId: int | None = None,
    dealId: int | None = None,
):
    payload = {
        "productId": productId,
        "quantity": quantity,
    }

    if contactId is not None:
        payload["contactId"] = contactId
    if dealId is not None:
        payload["dealId"] = dealId

    return payload


def payload_create_order_from_basket(
    *,
    productTypeId: int = 1,
    comment: str = "string",
    contactId: int,
    deliveryTypeId: int = 1,
    skipSend2SD: int = 1,
    date: str | None = None,
    userComment: str | None = None,
    description: str | None = None,
    address: str | None = None,
    couponId: int | None = None,
):
    payload = {
        "productTypeId": productTypeId,
        "comment": comment,
        "contactId": contactId,
        "deliveryTypeId": deliveryTypeId,
        "skipSend2SD": skipSend2SD,
    }

    if date is not None:
        payload["date"] = date
    if userComment is not None:
        payload["userComment"] = userComment
    if description is not None:
        payload["description"] = description
    if deliveryTypeId == 2 and address is not None:
        payload["address"] = address
    if couponId is not None:
        payload["couponId"] = couponId

    return payload
