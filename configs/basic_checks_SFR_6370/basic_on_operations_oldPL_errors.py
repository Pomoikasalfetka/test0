# Описание теста:
#
# Проверка ошибок при создании операции начисления (POST /v2/api/operations)
# для рекомендателя старой программы лояльности (21MAY202601@00001.ru).
#"Обновлённые условия" == НЕТ , "Исключать из автопересчета" == Нет
# Общий сценарий:
# 1. Тест 1: создаём контакт и карту (full_contact) — только перед первым тестом.
# 2. Показываем состояние сделки из Elastic (show_deal_info).
# 3. Пытаемся создать операцию начисления по проблемной сделке (create_operation)
#    и ожидаем ошибку (expected_status_code + expected_error_contains).
# 3. В конце всех тестов сбрасываем пользователя (reset_contact).
#
# Тест 1: в сделке пустой рекомендатель (sourceId = 9997689, ошибка 400).
# Тест 2: рекомендатель в сделке не совпадает с клиентом (sourceId = 9997785, ошибка 409).
# Тест 3: сделка не в статусе WON (sourceId = 9997937, ошибка 409).
# Тест 4: контакт клиента и рекомендатель в сделке совпадают (sourceId = 9998113, ошибка 409).
from configs.common_scenario_runners import SCENARIO_RUNNERS


RUN_CONFIGS = [
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 1: Делаем начисление по операции, в сделке пустой рекомендатель ",
        },
    },
    {   #https://corp.synergy.ru/crm/contact/details/4214433/
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
    {   #https://corp.synergy.ru/crm/deal/details/9997689/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9997689",
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9997689/
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "Operation error test",
            "comment": "Operation error test",
            "typeSourceId": 2,
            "sourceId": "9997689",
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
    {   #https://corp.synergy.ru/crm/deal/details/9997785/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9997785",
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9997785/
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "Operation error test",
            "comment": "Operation error test",
            "typeSourceId": 2,
            "sourceId": "9997785",
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
    {   #https://corp.synergy.ru/crm/deal/details/9997937/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9997937",
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9997937/
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "Operation error test",
            "comment": "Operation error test",
            "typeSourceId": 2,
            "sourceId": "9997937",
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
    {   #https://corp.synergy.ru/crm/deal/details/9998113/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9998113",
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9998113/
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "21MAY202601@00001.ru",
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "Operation error test",
            "comment": "Operation error test",
            "typeSourceId": 2,
            "sourceId": "9998113",
            "expected_status_code": 409,
            "expected_error_contains": "не должен совпадать с recommenderId",
        },
    },
     {
         "scenario": "reset_contact",
         "scenario_data": {
             "email": "21MAY202601@00001.ru",
         },
     },

]
