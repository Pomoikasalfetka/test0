import requests
import time
import jwt
from config import API_URL, LOGIN_ADMIN, PASSWORD_ADMIN

ADMIN_TOKEN = None
USER_TOKENS = {}


def _request_token(USER_EMAIL, USER_PASSWORD):
    head = {
        "Content-Type": "application/x-www-form-urlencoded",
        "grant_type": "password",
        "client_id": "public",
        "username": str(USER_EMAIL),
        "password": str(USER_PASSWORD),
        "scope": "openid email",
    }
    response = requests.post(API_URL, head, timeout=300)
    if response.status_code == 200:
        response_json = response.json()
        return response_json.get("access_token", None)

    print(f"Ошибка СОЗДАНИЯ #2 токена для пользователя: {USER_EMAIL}")
    return None

#Метод обновлет токен для пользователя . Если будет ошибка обновления то 
# вернется значение TOKEN = None
def Update_token(TOKEN , USER_EMAIL, USER_PASSWORD ):
    try:
        #Получает данные по токену без верификации (Декодируем), без сигнатуры
        decoded_payload = jwt.decode(TOKEN, options={"verify_signature": False})
    except jwt.exceptions.PyJWTError as e:  
        decoded_payload = None  
    if decoded_payload != None:
        #Достаем поле exp в котором хранится оставшиеся время работы токена
        exp_time = decoded_payload.get('exp', int(time.time()) )
        # Получаем текущие время и отнимаем 5*60 секунд (5 минут)
        current_time = int(time.time() - 300) 
        #readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(current_time))
        #Если текущие время - 300 секунд больше время из поля токена exp . то возращаем True что время вышло.
        if current_time > exp_time:
            TOKEN = _request_token(USER_EMAIL, USER_PASSWORD)
    else:
        TOKEN = None    
        print(f"Ошибка ВАЛИДАЦИИ #1 токена для пользователя: {USER_EMAIL}")           
    return TOKEN


def get_admin_token():
    global ADMIN_TOKEN

    if ADMIN_TOKEN is None:
        ADMIN_TOKEN = _request_token(LOGIN_ADMIN, PASSWORD_ADMIN)
        return ADMIN_TOKEN

    ADMIN_TOKEN = Update_token(ADMIN_TOKEN, LOGIN_ADMIN, PASSWORD_ADMIN)
    if ADMIN_TOKEN is None:
        ADMIN_TOKEN = _request_token(LOGIN_ADMIN, PASSWORD_ADMIN)
    return ADMIN_TOKEN

#Метод создает токен для пользователя . Если будет ошибка создания то 
# вернется значение access_token = None
def create_token(USER_EMAIL, USER_PASSWORD ): 
    if USER_EMAIL == LOGIN_ADMIN and USER_PASSWORD == PASSWORD_ADMIN:
        return get_admin_token()

    user_key = (str(USER_EMAIL), str(USER_PASSWORD))
    token = USER_TOKENS.get(user_key)
    if token is None:
        token = _request_token(USER_EMAIL, USER_PASSWORD)
        USER_TOKENS[user_key] = token
        return token

    token = Update_token(token, USER_EMAIL, USER_PASSWORD)
    if token is None:
        token = _request_token(USER_EMAIL, USER_PASSWORD)
    USER_TOKENS[user_key] = token
    return token

