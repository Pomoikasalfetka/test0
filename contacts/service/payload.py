def payload_create_contact(
    *,
    email: str = "avoid2021@yandex.ru",
    balance: int = 10000,
    active: int = 1,
):
    payload = {
        "email": email,
        "balance": balance,
        "active": active,
    }
    return payload


def payload_reset_contact(*, email: str):
    return {
        "email": email,
        "physicalCardStatus": "toErase",
        "eraseContact": 1,
        "admin": 1,
    }
