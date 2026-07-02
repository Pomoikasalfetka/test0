# Описание теста:
# https://jr.synergy.ru/browse/SFR-6370
#
# Проверка ошибок при перерасчёте статуса программы лояльности (POST /api/LPClientStatusHistory)
# для рекомендателя старой программы лояльности (21MAY202601@00001.ru).
#"Обновлённые условия" == НЕТ , "Исключать из автопересчета" == Нет
#
# Общий сценарий каждого теста:
# 1. Создаём контакт и карту (full_contact).
# 2. Создаём операцию начисления по валидной сделке sourceId = 9998425 (create_operation).
# 3. Меняем sourceId последней операции в БД на проблемную сделку (update_operation_source_id).
# 4. Показываем состояние проблемной сделки из Elastic (show_deal_info).
# 5. Запускаем перерасчёт статуса и ожидаем ошибку 409 (calculate_client_status).
# 6. Проверяем временную блокировку карты: status = 5 и comment в cardsmovement
#    (check_card_status).
# 7. Проверяем сообщение LP_STATUS_RECALC_B24 в Rabbit (check_rabbit_lp_status_recalc_b24).
# 8. Сбрасываем пользователя (reset_contact).
#
# Тест 1: сделка не в статусе WON (update sourceId → 9997937, ошибка 409).
# Тест 2-1: в сделке не заполнен рекомендатель (update sourceId → 9997689, ошибка 409).
# Тест 2-2: в сделке указан неверный рекомендатель (update sourceId → 9997785, ошибка 409).
# Тест 3: в сделке нет контакта (update sourceId → 9999067, ошибка 409).
# Тест 4 - не делаем - изменился источник операции
# Тест 5: контакт клиента и рекомендатель в сделке совпадают (update sourceId → 9998113, ошибка 409).

# В конце каждого активного теста сбрасываем пользователя.
from configs.common_scenario_runners import SCENARIO_RUNNERS


RUN_CONFIGS = [
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 1: сделка не в статусе WON",
        },
    },
    # Тест 1: при перерасчёте у клиента сделка не в статусе WON (sourceId → 9997937).
    { 
        "scenario": "full_contact",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "card_reason": "Test: create card",
            "card_type_id": 2,
            "card_subtype_id": 2,
            "card_number": "000500",
            "balance": 0,
        },
    },
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "LP status check test operation",
            "comment": "LP status check test operation",
            "typeSourceId": 2,
            "sourceId": "9998425",
        },
    },    
    {   #https://corp.synergy.ru/crm/deal/details/9997937/
        "scenario": "update_operation_source_id",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "fields": {
                "sourceId": "9997937",
            },
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9997937/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9997937",
        },
    },
    {
        "scenario": "calculate_client_status",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "expected_status_code": 409,
            "expected_error_contains": "должна быть в статусе WON",
        },
    },
    {
        "scenario": "check_card_status",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "status": 5,
            "expected_comment_contains": "Временная блокировка карты: не выполнены условия проверки операций для пересчёта статуса программы лояльности",
        },
    },
    {
        "scenario": "check_rabbit_lp_status_recalc_b24",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "expect_message": True,
            "delete_on_read": True,
        },
    },    
    {
        "scenario": "reset_contact",
         "scenario_data": {
            "email": "21MAY202601@00001.ru",
        },
    },
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 2-1: другой рекомендатель в сделке (Не заполнен рекомендатель)",
        },
    },
    # Тест 2-1: при перерасчёте в сделке не заполнен рекомендатель (sourceId → 9997689).
    {
        "scenario": "full_contact",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "card_reason": "Test: create card",
            "card_type_id": 2,
            "card_subtype_id": 2,
            "card_number": "000500",
            "balance": 0,
        },
    },
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "LP status check test operation",
            "comment": "LP status check test operation",
            "typeSourceId": 2,
            "sourceId": "9998425",
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9997689/
        "scenario": "update_operation_source_id",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "fields": {
                "sourceId": "9997689",
            },
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9997689/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9997689",
        },
    },
    {
        "scenario": "calculate_client_status",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "expected_status_code": 409,
            "expected_error_contains": "recommenderId должен совпадать с bitrixId клиента",
        },
    },
    {
        "scenario": "check_card_status",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "status": 5,
            "expected_comment_contains": "Временная блокировка карты: не выполнены условия проверки операций для пересчёта статуса программы лояльности",
        },
    },
    {
        "scenario": "check_rabbit_lp_status_recalc_b24",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "expect_message": True,
            "delete_on_read": True,
        },
    },
    {
        "scenario": "reset_contact",
         "scenario_data": {
            "email": "21MAY202601@00001.ru",
        },
    },  
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 2-2: другой рекомендатель в сделке (Не верный рекомендатель )",
        },
    },
    # Тест 2-2: при перерасчёте в сделке указан неверный рекомендатель (sourceId → 9997785).
    {
        "scenario": "full_contact",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "card_reason": "Test: create card",
            "card_type_id": 2,
            "card_subtype_id": 2,
            "card_number": "000500",
            "balance": 0,
        },
    },
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "LP status check test operation",
            "comment": "LP status check test operation",
            "typeSourceId": 2,
            "sourceId": "9998425",
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9997785/
        "scenario": "update_operation_source_id",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "fields": {
                "sourceId": "9997785",
            },
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9997785/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9997785",
        },
    },
    {
        "scenario": "calculate_client_status",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "expected_status_code": 409,
            "expected_error_contains": "recommenderId должен совпадать с bitrixId клиента",
        },
    },
    {
        "scenario": "check_card_status",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "status": 5,
            "expected_comment_contains": "Временная блокировка карты: не выполнены условия проверки операций для пересчёта статуса программы лояльности",
        },
    },
    {
        "scenario": "check_rabbit_lp_status_recalc_b24",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "expect_message": True,
            "delete_on_read": True,
        },
    },
    {
        "scenario": "reset_contact",
         "scenario_data": {
            "email": "21MAY202601@00001.ru",
        },
    },

    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 3: нет контакта в сделке",
        },
    },
    # Тест 3: при перерасчёте в сделке нет контакта (sourceId → 9999067).
    {
        "scenario": "full_contact",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "card_reason": "Test: create card",
            "card_type_id": 2,
            "card_subtype_id": 2,
            "card_number": "000500",
            "balance": 0,
        },
    },
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "LP status check test operation",
            "comment": "LP status check test operation",
            "typeSourceId": 2,
            "sourceId": "9998425",
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9999067/
        "scenario": "update_operation_source_id",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "fields": {
                "sourceId": "9999067",
            },
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9999067/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9999067",
        },
    },
    {
        "scenario": "calculate_client_status",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "expected_status_code": 409,
            "expected_error_contains": "bitrixId=undefined не найден в Elasticsearch",
        },
    },
    {
        "scenario": "check_card_status",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "status": 5,
            "expected_comment_contains": "Временная блокировка карты: не выполнены условия проверки операций для пересчёта статуса программы лояльности",
        },
    },
    {
        "scenario": "check_rabbit_lp_status_recalc_b24",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "expect_message": True,
            "delete_on_read": True,
        },
    },
    {
        "scenario": "reset_contact",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
        },
    },
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 5: Контакт и рекомендатель совпадают в сделке",
        },
    },
    # Тест 5: контакт клиента и рекомендатель в сделке совпадают (sourceId → 9998113).
    { 
        "scenario": "full_contact",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "card_reason": "Test: create card",
            "card_type_id": 2,
            "card_subtype_id": 2,
            "card_number": "000500",
            "balance": 0,
        },
    },
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "LP status check test operation",
            "comment": "LP status check test operation",
            "typeSourceId": 2,
            "sourceId": "9998425",
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9998113/
        "scenario": "update_operation_source_id",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "fields": {
                "sourceId": "9998113",
            },
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9998113/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9998113",
        },
    },
    {
        "scenario": "calculate_client_status",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "expected_status_code": 409,
            "expected_error_contains": "не должен совпадать с recommenderId",
        },
    },
    {
        "scenario": "check_card_status",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "status": 5,
            "expected_comment_contains": "Временная блокировка карты: не выполнены условия проверки операций для пересчёта статуса программы лояльности",
        },
    },
    {
        "scenario": "check_rabbit_lp_status_recalc_b24",
        "scenario_data": {
            "email": "21MAY202601@00001.ru",
            "expect_message": True,
            "delete_on_read": True,
        },
    },
    {
        "scenario": "reset_contact",
         "scenario_data": {
            "email": "21MAY202601@00001.ru",
        },
    },    

]
