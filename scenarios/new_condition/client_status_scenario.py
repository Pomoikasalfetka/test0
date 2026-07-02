from db.mysql_client import get_contact_id_by_email
from new_condition.service.methods_service import (
    calculate_LPClientStatusHistory as post_LPClientStatusHistory,
)
from new_condition.service.payload import payload_calculate_client_status


def calculate_LPClientStatusHistory(*, email: str, headers):
    # Расчет статуса клиента по email:
    # 1. Находит contactId в БД (таблица contacts).
    # 2. Вызывает POST /api/LPClientStatusHistory для расчета статуса.
    # 3. Возвращает contactId, statusId и полный ответ сервиса.
    contact_id = get_contact_id_by_email(email)
    payload = payload_calculate_client_status(contactId=contact_id)
    result = post_LPClientStatusHistory(
        payload=payload,
        headers=headers,
        raw_response=False,
    )
    status_id = result["response"]["statusId"]
    return contact_id, status_id, result
