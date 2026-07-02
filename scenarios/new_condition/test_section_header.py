import logging

from colorama import Fore

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_section_header_scenario(*, scenario_data):
    text = scenario_data["text"]

    logger.info(
        Fore.BLUE + f"\n\n{'=' * 60}\n{text}\n{'=' * 60}\n",
    )
    return {
        "text": text,
    }
