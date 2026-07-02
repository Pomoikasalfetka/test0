from config import TIMEOUT, B24_SERVER
import requests
from response_handler import assert_ok_and_get_json

ELASTIC_PROVIDERS_URL = f"{B24_SERVER}/api/entity/loyalty-partners/"

#Ожидаемые значения для парнеров в Б24 
# Данные Б24 https://corp.synergy.ru/bitrix/admin/highloadblock_rows_list.php?ENTITY_ID=66&lang=ru - но пока не точно
WATING_RESULT_PROVIDERS = [
    {
        "id": 1,
        "name": "Synergy Friends",
        "referralLand": {
        "id": 1,
        "value": "sf_referral_land"
        },
        "showInAddCard": 1,
        "uf_id": "00001"
    },
    {
        "id": 4,
        "name": "Synergy Store",
        "showInAddCard": 0,
        "uf_id": "00004"
    },
    {
        "id": 5,
        "name": "MOI Capital",
        "referralLand": {
        "id": 6,
        "value": "mc_referral_land"
        },
        "showInAddCard": 1,
        "uf_id": "00005"
    },
    {
        "id": 6,
        "name": "Mosap Team",
        "referralLand": {
        "id": 7,
        "value": "mt_referral_land"
        },
        "showInAddCard": 1,
        "uf_id": "00006"
    }
    ]

def get_elastic_loyalaty_partners(ID):
    response = requests.get(
        ELASTIC_PROVIDERS_URL + str(ID),
        headers=None,
        json=None,
        timeout=TIMEOUT,
    )
    return assert_ok_and_get_json(response, f"get loyalty partner {ID}")
