# Описание теста:
# Создаем пользователя, делаем операцию начисления и аннулируем эту операцию.
# Проверки выполняются по таблице lpstatushistory (active = 1) без перерасчета.
# После начисления ожидаем statusId 25 (BestFriend), countOps 1, dateOfDemotion = текущая дата + 6 мес.
# После аннулирования ожидаем statusId 23 (Friend).
# В конце сбрасываем пользователя.
from configs.common_scenario_runners import SCENARIO_RUNNERS


RUN_CONFIGS = [
        {
        "scenario": "full_contact",
        "scenario_data": {
            # Test user created per SFR-6400.
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
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "Annulation test operation",
            "comment": "Annulation test operation",
            "typeSourceId": 2,
            "sourceId": "9963635",
        },
    },
    {
        "scenario": "check_contact_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "statusId": 25,
        },
    },
    {
        "scenario": "check_contact_count_ops",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "countOps": 1,
        },
    }, 
    {
        "scenario": "check_contact_date_of_demotion",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "months": 6,
        },
    },        
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "operationId": 10,
            "type": "Списание",
            "clientStatusId": 25,
            "description": "Аннулирование",
            "amount": 700,
            "partner": "000001",
            "reason": "Annulation test operation",
            "comment": "Annulation test operation",
            "typeSourceId": 2,
            "sourceId": "9963635",
            "canceledOperationIds": "D_9963635",
        },
    },
    {
        "scenario": "check_contact_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "statusId": 23,
        },
    },   
    #{
    #    "scenario": "reset_contact",
    #    "scenario_data": {
    #        "email": "test-user-2@bazatletika.ru",
    #    },
    #},
]
