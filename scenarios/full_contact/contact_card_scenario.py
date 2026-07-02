from cards.service.methods_service import create_card, link_user_and_card
from cards.service.payload import payload_create_card
from contacts.service.methods_service import create_contact
from contacts.service.payload import payload_create_contact


def create_full_contact(
    *,
    headers,
    email: str,
    card_number: str,
    type_id: int,
    subtype_id: int,
    reason: str,
    balance: int = 100000,
    active: int = 1,
):
    contact_payload = payload_create_contact(
        email=email,
        balance=balance,
        active=active,
    )
    contact_response = create_contact(
        payload=contact_payload,
        headers=headers,
        raw_response=False,
    )

    contact_info = contact_response["response"]["contact"][0]
    prepared_contact = {
        "id": contact_info["id"],
        "email": contact_info["email"],
        "balance": contact_info["balance"]
    }

    card_payload = payload_create_card(
        reason=reason,
        typeId=type_id,
        subTypeId=subtype_id,
        cardNumber=card_number,
    )
    card_response = create_card(
        payload=card_payload,
        headers=headers,
        raw_response=False,
    )

    card_info = card_response["response"]["cards"][0]
    prepared_card = {
        "id": card_info["id"],
        "cardNumber": card_info["cardNumber"],
    }

    link_response = link_user_and_card(
        card_id=prepared_card["id"],
        email_user=email,
        headers=headers,
        raw_response=False,
    )

    link_info = link_response["response"]["card"]
    prepared_link_card = {
        "id": link_info["id"],
        "cardNumber": link_info["cardNumber"],
        "email": link_info["email"],
        "typeId": link_info["typeId"],
        "subTypeId": link_info["subTypeId"],
        "status": link_info["status"],
    }

    return {
        "contact_payload": contact_payload,
        "contact_response": contact_response,
        "contact": prepared_contact,
        "card_payload": card_payload,
        "card_response": card_response,
        "card": prepared_card,
        "link": prepared_link_card,
    }
