# Описание теста:
# https://jr.synergy.ru/browse/SFR-6370
#
# Проверка ошибок при перерасчёте статуса программы лояльности (POST /api/LPClientStatusHistory)
# для рекомендателя, участвующего в новых условиях ПЛ.
# "Обновлённые условия" == ДА , "Исключать из автопересчета" == Нет
# 
# Общий сценарий каждого теста:
# 1. Создаём контакт и карту (full_contact).
# 2. Создаём операцию начисления по валидной сделке (create_operation).
# 3. Меняем данные последней операции в БД на тестовые (update_operation_source_id).
# 4. Показываем состояние проблемной сделки из Elastic (show_deal_info).
# 5. Запускаем перерасчёт статуса и ожидаем ошибку 409 (calculate_client_status).
# 6. Проверяем временную блокировку карты: status = 5 и comment в cardsmovement
#    (check_card_status).
# 7. Сбрасываем пользователя (reset_contact).
#
# Тест 1: сделка не в статусе WON (sourceId = 9998913).
# Тест 2-1: в сделке не заполнен рекомендатель (sourceId = 9992017).
# Тест 2-2: в сделке указан неверный рекомендатель (sourceId = 9995581).
# Тест 3: в сделке нет контакта (sourceId = 6363089).
# Тест 4: изменился источник операции — не сделка (source = C_9963635, typeSourceId = 3).
# Тест 5: контакт клиента и рекомендатель в сделке совпадают (sourceId = 9994693).
#
# В конце каждого теста сбрасываем пользователя.
from configs.common_scenario_runners import SCENARIO_RUNNERS


RUN_CONFIGS = [
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 1: сделка не в статусе WON",
        },
    },
    #Первый тест - когда при перерасчете методом - у клиента есть сделка с ошибкой 
    #(статус сделки не WON) - Рекомендатель участвует в новых условиях ПЛ
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
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "LP status check test operation",
            "comment": "LP status check test operation",
            "typeSourceId": 2,
            "sourceId": "9963635",
        },
    },    
    {   #https://corp.synergy.ru/crm/contact/details/4114005/
        #https://corp.synergy.ru/crm/deal/details/9998913/    
        "scenario": "update_operation_source_id",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "fields": {
                "sourceId": "9998913",
            },
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9998913/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9998913",
        },
    },
    {
        "scenario": "calculate_client_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "expected_status_code": 409,
            "expected_error_contains": "должна быть в статусе WON",
        },
    },
    {
        "scenario": "check_card_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "status": 5,
            "expected_comment_contains": "Временная блокировка карты: не выполнены условия проверки операций для пересчёта статуса программы лояльности",
        },
    },
    {
        "scenario": "reset_contact",
         "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
        },
    },
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 2-1: другой рекомендатель в сделке (Не заполнен рекомендатель)",
        },
    },
    #Второй тест - когда при перерасчете методом , есть ошибка по сделке , 
    #стоит другой рекомендатель - Рекомендатель участвует в новых условиях ПЛ
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
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "LP status check test operation",
            "comment": "LP status check test operation",
            "typeSourceId": 2,
            "sourceId": "9963635",
        },
    },
    {   #https://corp.synergy.ru/crm/contact/details/4207258/
        #https://corp.synergy.ru/crm/deal/details/9992017/   
        "scenario": "update_operation_source_id",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "fields": {
                "sourceId": "9992017",
            },
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9992017/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9992017",
        },
    },
    {
        "scenario": "calculate_client_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "expected_status_code": 409,
            "expected_error_contains": "recommenderId должен совпадать с bitrixId клиента",
        },
    },
    {
        "scenario": "check_card_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "status": 5,
            "expected_comment_contains": "Временная блокировка карты: не выполнены условия проверки операций для пересчёта статуса программы лояльности",
        },
    },
    {
        "scenario": "reset_contact",
         "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
        },
    },  
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 2-2: другой рекомендатель в сделке (Не верный рекомендатель )",
        },
    },
    #Второй тест - когда при перерасчете методом , есть ошибка по сделке , 
    #стоит другой рекомендатель - Рекомендатель участвует в новых условиях ПЛ
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
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "LP status check test operation",
            "comment": "LP status check test operation",
            "typeSourceId": 2,
            "sourceId": "9963635",
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9995581/ 
        "scenario": "update_operation_source_id",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "fields": {
                "sourceId": "9995581",
            },
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9995581/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9995581",
        },
    },
    {
        "scenario": "calculate_client_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "expected_status_code": 409,
            "expected_error_contains": "recommenderId должен совпадать с bitrixId клиента",
        },
    },
    {
        "scenario": "check_card_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "status": 5,
            "expected_comment_contains": "Временная блокировка карты: не выполнены условия проверки операций для пересчёта статуса программы лояльности",
        },
    },
    {
        "scenario": "reset_contact",
         "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
        },
    },  

    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 3: нет контакта в сделке",
        },
    },
    #Третий тест - когда при перерасчете методом , нет контакта в сделке 
    #Рекомендатель участвует в новых условиях ПЛ
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
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "LP status check test operation",
            "comment": "LP status check test operation",
            "typeSourceId": 2,
            "sourceId": "9963635",
        },
    },
    {   
        #https://corp.synergy.ru/crm/deal/details/6363089/   
        "scenario": "update_operation_source_id",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "fields": {
                "sourceId": "6363089",
            },
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/6363089/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "6363089",
        },
    },
    {
        "scenario": "calculate_client_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "expected_status_code": 409,
            "expected_error_contains": "bitrixId=undefined не найден в Elasticsearch",
        },
    },
    {
        "scenario": "check_card_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "status": 5,
            "expected_comment_contains": "Временная блокировка карты: не выполнены условия проверки операций для пересчёта статуса программы лояльности",
        },
    },
    {
        "scenario": "reset_contact",
         "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
        },
    },    
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 4: Изменился источник ИД операции по сделке",
        },
    },
    #Четвертый тест - когда у клиента поменялся тип операции(что насамом дела просто мало вероятно) 
    #Рекомендатель участвует в новых условиях ПЛ
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
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "LP status check test operation",
            "comment": "LP status check test operation",
            "typeSourceId": 2,
            "sourceId": "9963635",
        },
    },
    {    
        "scenario": "update_operation_source_id",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "fields": {
                "source": "C_9963635",
                "typeSourceId": 3,
            },
        },
    },
    {
        "scenario": "calculate_client_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "expected_status_code": 409,
            "expected_error_contains": "источник операции должен быть сделка",
        },
    },
    {
        "scenario": "check_card_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "status": 5,
            "expected_comment_contains": "Временная блокировка карты: не выполнены условия проверки операций для пересчёта статуса программы лояльности",
        },
    },
    {
        "scenario": "reset_contact",
         "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
        },
    },    
    {
        "scenario": "section_header",
        "scenario_data": {
            "text": "Тест 5: Контакт и рекомендатель совпадают в сделке",
        },
    },
    #Пятый тест - когда контакт рекомендателя и контакт клиента совпадают в сделке
    #Рекомендатель участвует в новых условиях ПЛ
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
            "operationId": 3,
            "type": "Начисление",
            "clientStatusId": 23,
            "description": "За покупку академ товара",
            "amount": 700,
            "partner": "000001",
            "reason": "LP status check test operation",
            "comment": "LP status check test operation",
            "typeSourceId": 2,
            "sourceId": "9963635",
        },
    },
    {    
        "scenario": "update_operation_source_id",
        "scenario_data": {
            "card_email": "test-user-2@bazatletika.ru",
            "fields": {
                "sourceId": "9994693",
            },
        },
    },
    {   #https://corp.synergy.ru/crm/deal/details/9994693/
        "scenario": "show_deal_info",
        "scenario_data": {
            "deal_id": "9994693",
        },
    },
    {
        "scenario": "calculate_client_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "expected_status_code": 409,
            "expected_error_contains": "не должен совпадать с recommenderId",
        },
    },
    {
        "scenario": "check_card_status",
        "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
            "status": 5,
            "expected_comment_contains": "Временная блокировка карты: не выполнены условия проверки операций для пересчёта статуса программы лояльности",
        },
    },
    {
        "scenario": "reset_contact",
         "scenario_data": {
            "email": "test-user-2@bazatletika.ru",
        },
    },    

]
