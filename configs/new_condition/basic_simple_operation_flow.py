# Описание теста:
# Создаем пользователя и прогоняем операции, которые не повышают статус клиента, но заносятся в lpstatushistory
# После каждой операции проверяем поля lpstatushistory (active = 1), в том числе
# lastAddOperationId — что последняя операция отображается корректно.
#Операции берутся из ПЛ: Настройки валидации -> Активность до 6 мес == ДА 
# Так же учитваем минимальную сумму оплаты для внесения в таблицу расчета lpstatushistory
# Ограничение по сумме = <Значение>
#(Пока не используем Поощрение за привлечение клиента == ДА)
#Приказ (1)- Оплата обучения по СЗ (500)- Оплата у партнёра (500)- За товары по СЗ	(500)	
#- Оплата обучения из ЛК (500)- За товары из ЛК (500)
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
    #Первая операция и проверки по ней.
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "operationId": 7,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "Приказ",
            "amount": 9999,
            "partner": "000001",
            "reason": "Create user operation test",
            "comment": "Create user operation test",
            "typeSourceId": 3,
            "sourceId": "7135605",
        },
    }, 
    {
        "scenario": "check_contact_last_add_operation_id",
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
    #Вторая операция и проверки по ней.
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "operationId": 2,
            "type": "Списание",
            "clientStatusId": 23,
            "description": "Оплата обучения по СЗ",
            "amount": 500,
            "partner": "000001",
            "reason": "Create user operation test",
            "comment": "Create user operation test",
            "typeSourceId": 3,
            "sourceId": "7135605",
        },
    }, 
    {
        "scenario": "check_contact_last_add_operation_id",
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
    #Третья операция и проверки по ней.
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "operationId": 46,
            "type": "Списание",
            "clientStatusId": 23,
            "description": "За товары из ЛК",
            "amount": 500,
            "partner": "000001",
            "reason": "Create user operation test",
            "comment": "Create user operation test",
            "typeSourceId": 3,
            "sourceId": "7135605",
        },
    }, 
    {
        "scenario": "check_contact_last_add_operation_id",
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
    #Четвертая операция и проверки по ней.
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "operationId": 11,
            "type": "Списание",
            "clientStatusId": 23,
            "description": "Оплата у партнёра",
            "amount": 500,
            "partner": "000001",
            "reason": "Create user operation test",
            "comment": "Create user operation test",
            "typeSourceId": 3,
            "sourceId": "7135605",
        },
    }, 
    {
        "scenario": "check_contact_last_add_operation_id",
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
    #Пятая операция и проверки по ней.
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "operationId": 4,
            "type": "Списание",
            "clientStatusId": 23,
            "description": "За товары по СЗ",
            "amount": 500,
            "partner": "000001",
            "reason": "Create user operation test",
            "comment": "Create user operation test",
            "typeSourceId": 3,
            "sourceId": "7135605",
        },
    }, 
    {
        "scenario": "check_contact_last_add_operation_id",
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
    #Шестая операция и проверки по ней.
    {
        "scenario": "create_operation",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "operationId": 45,
            "type": "Списание",
            "clientStatusId": 23,
            "description": "Оплата обучения из ЛК",
            "amount": 500,
            "partner": "000001",
            "reason": "Create user operation test",
            "comment": "Create user operation test",
            "typeSourceId": 3,
            "sourceId": "7135605",
        },
    }, 
    {
        "scenario": "check_contact_last_add_operation_id",
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
