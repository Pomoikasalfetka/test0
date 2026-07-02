# Описание теста:
#
# Проверка ошибок при создании операции начисления (POST /v2/api/operations)
# для рекомендателя, участвующего в новых условиях ПЛ.
#
# Общий сценарий каждого теста:
# 1. Создаём контакт и карту (full_contact) — только перед первым тестом.
# 2. Показываем состояние сделки из Elastic (show_deal_info).
# 3. Пытаемся создать операцию начисления по проблемной сделке (create_operation)
#    и ожидаем ошибку (expected_status_code + expected_error_contains).
# 4. В конце всех тестов сбрасываем пользователя (reset_contact).
#
# Тест 1: в сделке пустой рекомендатель (sourceId = 9992017, ошибка 400).
# Тест 2: рекомендатель в сделке не совпадает с клиентом (sourceId = 9995581, ошибка 409).
# Тест 3: сделка не в статусе WON (sourceId = 6369045, ошибка 409).
# Тест 4: контакт клиента и рекомендатель в сделке совпадают (sourceId = 9994693, ошибка 409).
# Тест 5: в сделке нет контакта (sourceId = 6363089, ошибка 409).
#
# В конце каждого теста сбрасываем пользователя.
from configs.common_scenario_runners import SCENARIO_RUNNERS


RUN_CONFIGS = [
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 1: Делаем начисление по операции, в сделке пустой рекомендатель ",
        },
    },    
    {
        "scenario": "full_contact",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "card_reason": "Test: create card",
            "card_type_id": 2,
            "card_subtype_id": 2,
            "card_number": "000500",
            "balance": 0,
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9992017/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9992017",
        },
    },
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "Operation error test",
            "comment": "Operation error test",
            "typeSourceId": 2,
            "sourceId": "9992017",
            "expected_status_code": 400,
            "expected_error_contains": "В сделке отсутствуют данные о рекомендателе",
        },
    },
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 2: Делаем начисление по операции, не соответсвует рекомендатель в сделке ",
        },
    },    
    {   #https://corp.synergy.ru/crm/deal/details/9995581/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9995581",
        },
    },
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "Operation error test",
            "comment": "Operation error test",
            "typeSourceId": 2,
            "sourceId": "9995581",
            "expected_status_code": 409,
            "expected_error_contains": "recommenderId должен совпадать с bitrixId клиента",
        },
    },
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 3: Сделка не в статусе WON ",
        },
    },    
    {   #https://corp.synergy.ru/crm/deal/details/6369045/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "6369045",
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/6369045/
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "Operation error test",
            "comment": "Operation error test",
            "typeSourceId": 2,
            "sourceId": "6369045",
            "expected_status_code": 409,
            "expected_error_contains": "Транзакция отклонена. Сделка в недопустимом статусе",
        },
    },
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 4: Рекомендатель и контакт в сделке совпадают ",
        },
    },    
    {   #https://corp.synergy.ru/crm/deal/details/9994693/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9994693",
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9994693/
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "Operation error test",
            "comment": "Operation error test",
            "typeSourceId": 2,
            "sourceId": "9994693",
            "expected_status_code": 409,
            "expected_error_contains": "не должен совпадать с recommenderId",
        },
    },
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 5: нет контакта в сделке",
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/6363089/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "6363089",
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/6363089/
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "Operation error test",
            "comment": "Operation error test",
            "typeSourceId": 2,
            "sourceId": "6363089",
            "expected_status_code": 409,
            "expected_error_contains": "bitrixId=undefined не найден в Elasticsearch",
        },
    },
    {
        "scenario": "reset_contact",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
        },
    },

]
