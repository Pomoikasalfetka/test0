import logging

from colorama import Fore

from authorization_token import get_admin_token
from contacts.service.methods_service import reset_contact
from contacts.service.payload import payload_reset_contact

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_reset_contact_scenario(*, scenario_data):
    email = scenario_data["email"]

    token = get_admin_token()
    admin_headers = {"Authorization": f"Bearer {token}"}

    payload = payload_reset_contact(email=email)
    result = reset_contact(
        payload=payload,
        headers=admin_headers,
        raw_response=False,
    )

    logger.info(
        Fore.GREEN + f"\nContact reset completed: email={email}",
    )
    return {
        "email": email,
        "response": result,
    }
