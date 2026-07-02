import base64
import json
import time
import urllib.error
import urllib.parse
import urllib.request

from config import (
    RABBIT_MANAGEMENT_PORT,
    RABBIT_PASSWORD,
    RABBIT_SERVER_HOST,
    RABBIT_SERVER_QUEUE_05,
    RABBIT_USER,
)


def _management_request(*, method: str, path: str, payload: dict | None = None):
    url = f"http://{RABBIT_SERVER_HOST}:{RABBIT_MANAGEMENT_PORT}{path}"
    headers = {
        "Authorization": "Basic "
        + base64.b64encode(f"{RABBIT_USER}:{RABBIT_PASSWORD}".encode()).decode(),
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode()

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode()
            if not body:
                return None
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        raise AssertionError(
            f"RabbitMQ management API error: status={exc.code} url={url} body={exc.read().decode()}"
        ) from exc
    except urllib.error.URLError as exc:
        raise AssertionError(
            f"RabbitMQ management API is unavailable at {RABBIT_SERVER_HOST}:{RABBIT_MANAGEMENT_PORT}: {exc.reason}"
        ) from exc


def get_messages_from_queue(*, queue: str, count: int = 10, delete_on_read: bool = True) -> list[dict]:
    ackmode = "ack_requeue_false" if delete_on_read else "ack_requeue_true"
    encoded_queue = urllib.parse.quote(queue, safe="")
    result = _management_request(
        method="POST",
        path=f"/api/queues/%2F/{encoded_queue}/get",
        payload={
            "count": count,
            "ackmode": ackmode,
            "encoding": "auto",
        },
    )
    if not result:
        return []

    messages = []
    for item in result:
        payload = item.get("payload")
        if payload is None:
            continue
        if isinstance(payload, str):
            messages.append(json.loads(payload))
        else:
            messages.append(payload)
    return messages


def _normalize_id(value) -> int:
    return int(value)


def find_lp_status_recalc_b24_message(
    *,
    contact_id: int,
    card_id: int | None = None,
    queue: str = RABBIT_SERVER_QUEUE_05,
    event_name: str = "LP_STATUS_RECALC_B24",
    timeout_seconds: float = 10,
    poll_interval: float = 0.5,
    delete_on_read: bool = True,
) -> dict | None:
    expected_contact_id = _normalize_id(contact_id)
    expected_card_id = _normalize_id(card_id) if card_id is not None else None

    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        messages = get_messages_from_queue(
            queue=queue,
            count=1,
            delete_on_read=delete_on_read,
        )
        if not messages:
            time.sleep(poll_interval)
            continue

        message = messages[0]
        if message.get("event_name") != event_name:
            continue
        data = message.get("data") or {}
        if "contactId" not in data:
            continue
        if _normalize_id(data["contactId"]) != expected_contact_id:
            continue
        if expected_card_id is not None:
            if "cardId" not in data:
                continue
            if _normalize_id(data["cardId"]) != expected_card_id:
                continue
        return message
    return None
