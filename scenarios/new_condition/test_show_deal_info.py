import logging

import requests
from colorama import Fore

from config import B24_SERVER, TIMEOUT
from response_handler import assert_ok_and_get_json

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def _resolve_deal_id(*, scenario_data) -> str:
    deal_id = scenario_data.get("deal_id") or scenario_data.get("sourceId")
    if deal_id is None:
        raise AssertionError("Pass deal_id or sourceId in scenario_data.")
    return str(deal_id)


def run_show_deal_info_scenario(*, scenario_data):
    deal_id = _resolve_deal_id(scenario_data=scenario_data)
    url = f"{B24_SERVER}/api/entity/deal/{deal_id}"

    response = requests.get(url, timeout=TIMEOUT)
    deal = assert_ok_and_get_json(response, f"get deal {deal_id}")

    stage = deal.get("stage") or {}
    contacts = deal.get("contacts") or []
    recommender_id = deal.get("recommenderId")

    lines = [
        f"Сделка id={deal.get('id', deal_id)}, docNum={deal.get('docNum', '—')}, title={deal.get('title', '—')}",
        f"stage.id: {stage.get('id', '—')}",
        f"stage.name: {stage.get('name', '—')}",
        f"recommenderId: {recommender_id if recommender_id is not None else '—'}",
        "contacts:",
    ]

    if contacts:
        for contact in contacts:
            contact_id = contact.get("id", "—")
            contact_title = contact.get("title", "—")
            primary = contact.get("primary")
            primary_label = " (primary)" if primary else ""
            lines.append(f"  - id: {contact_id}{primary_label}, title: {contact_title}")
    else:
        lines.append("  — нет контактов в сделке")

    output = "\n".join(lines)
    logger.info(Fore.CYAN + f"\n--- Состояние сделки {deal_id} ---\n{output}\n")

    return {
        "dealId": deal.get("id", deal_id),
        "docNum": deal.get("docNum"),
        "title": deal.get("title"),
        "stageId": stage.get("id"),
        "stageName": stage.get("name"),
        "recommenderId": recommender_id,
        "contacts": contacts,
        "rawDeal": deal,
    }
