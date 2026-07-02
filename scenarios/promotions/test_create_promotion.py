import logging
import unittest

from colorama import Fore

from authorization_token import get_admin_token
from promotions.service.methods_service import create_promotion
from promotions.service.payload import payload_create_promotion

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def _extract_promotion(result):
    response = result.get("response")
    if not isinstance(response, dict):
        return None

    promotions = response.get("promotions")
    if isinstance(promotions, list) and promotions:
        return promotions[0]

    promotion = response.get("promotion")
    if isinstance(promotion, dict):
        return promotion

    if isinstance(response, dict) and "id" in response:
        return response

    return None


def run_create_promotion_scenario(*, scenario_data):
    token = get_admin_token()
    admin_headers = {"Authorization": f"Bearer {token}"}
    testcase = unittest.TestCase()

    #logger.info(
    #    Fore.YELLOW + "\nCreate promotion, inline scenario_data",
    #)

    payload = payload_create_promotion(
        name=scenario_data["name"],
        startDate=scenario_data["startDate"],
        endDate=scenario_data["endDate"],
        activationConditionId=scenario_data["activationConditionId"],
        couponApplicationTypeId=scenario_data["couponApplicationTypeId"],
        couponNominal=scenario_data["couponNominal"],
        loyaltyProgramId=scenario_data["loyaltyProgramId"],
        active=scenario_data["active"],
        couponCodeLength=scenario_data["couponCodeLength"],
        description=scenario_data.get("description"),
        couponName=scenario_data.get("couponName"),
        couponValidityDays=scenario_data.get("couponValidityDays"),
        couponCodeCharset=scenario_data.get("couponCodeCharset"),
        couponCodePrefix=scenario_data.get("couponCodePrefix"),
        comment=scenario_data.get("comment"),
    )

    result = create_promotion(
        payload=payload,
        headers=admin_headers,
        raw_response=False,
    )

    promotion = _extract_promotion(result)
    if promotion is not None:
        if "name" in promotion:
            testcase.assertEqual(scenario_data["name"], promotion["name"])
        if "active" in promotion:
            testcase.assertEqual(scenario_data["active"], promotion["active"])
        if "activationConditionId" in promotion:
            testcase.assertEqual(
                scenario_data["activationConditionId"],
                promotion["activationConditionId"],
            )
        if "couponApplicationTypeId" in promotion:
            testcase.assertEqual(
                scenario_data["couponApplicationTypeId"],
                promotion["couponApplicationTypeId"],
            )
        if "loyaltyProgramId" in promotion:
            testcase.assertEqual(
                scenario_data["loyaltyProgramId"],
                promotion["loyaltyProgramId"],
            )

    logger.info(
        Fore.GREEN + f"\nPromotion created: name={scenario_data['name']} couponNominal={scenario_data['couponNominal']} activationConditionId={scenario_data['activationConditionId']} couponApplicationTypeId={scenario_data['couponApplicationTypeId']}",
    )
    return result
