import json


def assert_ok_and_get_json(response, action_name: str):
    if not response.ok:
        raise AssertionError(
            f"Failed to {action_name}: {response.status_code} {response.text}"
        )

    try:
        return response.json()
        
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"Failed to decode JSON after {action_name}: "
            f"{response.status_code} {response.text}"
        ) from exc
