def payload_create_promotion(
    *,
    name: str = "Test promotion",
    startDate: str = "2026-05-04T00:00:00Z",
    endDate: str = "2026-12-31T23:59:59Z",
    activationConditionId: int = 1,
    couponApplicationTypeId: int = 1,
    couponNominal: int | float = 1000,
    loyaltyProgramId: int = 1,
    active: int = 1,
    couponCodeLength: int = 8,
    description: str | None = None,
    couponName: str | None = None,
    couponValidityDays: int | None = None,
    couponCodeCharset: str | None = None,
    couponCodePrefix: str | None = None,
    comment: str | None = None,
):
    payload = {
        "name": name,
        "startDate": startDate,
        "endDate": endDate,
        "activationConditionId": activationConditionId,
        "couponApplicationTypeId": couponApplicationTypeId,
        "couponNominal": couponNominal,
        "loyaltyProgramId": loyaltyProgramId,
        "active": active,
        "couponCodeLength": couponCodeLength,
    }

    if description is not None:
        payload["description"] = description
    if couponName is not None:
        payload["couponName"] = couponName
    if couponValidityDays is not None:
        payload["couponValidityDays"] = couponValidityDays
    if couponCodeCharset is not None:
        payload["couponCodeCharset"] = couponCodeCharset
    if couponCodePrefix is not None:
        payload["couponCodePrefix"] = couponCodePrefix
    if comment is not None:
        payload["comment"] = comment

    return payload


def payload_create_coupons(
    *,
    promotionId: int,
    emails: list[str],
    jiraRequestId: str,
    comment: str | None = None,
):
    payload = {
        "promotionId": promotionId,
        "emails": emails,
        "jiraRequestId": jiraRequestId,
    }

    if comment is not None:
        payload["comment"] = comment

    return payload
