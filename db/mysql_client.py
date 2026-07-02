import pymysql

from config import (
    MYSQL_DATABASE,
    MYSQL_HOST,
    MYSQL_PASSWORD,
    MYSQL_PORT,
    MYSQL_USER,
)


def get_mysql_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
    )


def fetch_all(query: str, params: tuple | None = None):
    with get_mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()


def execute(query: str, params: tuple | None = None) -> int:
    with get_mysql_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            connection.commit()
            return cursor.lastrowid


def get_contact_id_by_email(email: str) -> int:
    # Ищет контакт в dbonlyfortest.contacts по email и возвращает его id.
    rows = fetch_all(
        "SELECT id FROM contacts WHERE email = %s LIMIT 1",
        (email,),
    )
    if not rows:
        raise AssertionError(f"Contact was not found by email={email}")
    return rows[0]["id"]


def get_card_id_by_email(email: str) -> int:
    # Ищет карту в dbonlyfortest.cards по email контакта и возвращает cardId.
    contact_id = get_contact_id_by_email(email)
    rows = fetch_all(
        "SELECT id FROM cards WHERE contactId = %s LIMIT 1",
        (contact_id,),
    )
    if not rows:
        raise AssertionError(f"Card was not found for email={email}")
    return rows[0]["id"]


def get_latest_cardsmovement_comment_by_card_id(*, card_id: int) -> str:
    rows = fetch_all(
        """
        SELECT comment
        FROM cardsmovement
        WHERE cardId = %s
        ORDER BY id DESC
        LIMIT 1
        """,
        (card_id,),
    )
    if not rows:
        raise AssertionError(f"Cards movement was not found for cardId={card_id}")
    return rows[0]["comment"]


def fetch_table(*, table: str, limit: int | None = None):
    query = f"SELECT * FROM {table}"
    if limit is not None:
        query += " LIMIT %s"
        return fetch_all(query, (limit,))
    return fetch_all(query)
