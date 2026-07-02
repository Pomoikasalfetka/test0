def payload_create_provider(
    *,
    description: str = "Тестовый поставщик",
    name: str = "Тестовый поставщик",
    partnerId: int = 1
):
    payload = {
        "description": description,
        "name": name,
        "partnerId": partnerId
    }
    return payload     
