# Описание теста:
# Создаем пользователя, делаем операцию начисления (Приказ) и запускаем перерасчет статуса.
# Тест проверяет создание записи в lpstatushistory после перерасчета.
# Проверки по таблице lpstatushistory (active = 1) без перерасчета:
# statusId 23 (Friend), countOps 0, lockDate 2020-01-01,
# tokenBurnDate = текущая дата + 18 мес., dateOfDemotion = null.
# В конце сбрасываем пользователя.
from configs.common_scenario_runners import SCENARIO_RUNNERS


RUN_CONFIGS = [
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
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "operationId": 7,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "Приказ",
            "amount": 599,
            "partner": "000001",
            "reason": "Create user operation test",
            "comment": "Create user operation test",
            "typeSourceId": 3,
            "sourceId": "7135605",
        },
    },
    {
        "scenario": "calculate_client_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
        },
    },
    {
        "scenario": "check_contact_count_ops",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "countOps": 0,
        },
    },    
    {
        "scenario": "check_contact_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "statusId": 23,
        },
    },
    {
        "scenario": "check_contact_lock_date",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "lockDate": "2020-01-01",
        },
    },
    {
        "scenario": "check_contact_token_burn_date",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "months": 18,
        },
    },  
    {
        "scenario": "check_contact_date_of_demotion",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "months": None,
        },
    },      
    {
        "scenario": "reset_contact",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
        },
    },
]
