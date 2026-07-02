import logging
import time

from colorama import Fore

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_delay_scenario(*, scenario_data):
    # Задержка выполнения теста на указанное количество секунд.
    seconds = scenario_data["seconds"]

    logger.info(
        Fore.YELLOW + f"\nDelay test started: {seconds} seconds",
    )
    time.sleep(seconds)
    logger.info(
        Fore.GREEN + f"\nDelay test completed: {seconds} seconds",
    )
    return {
        "seconds": seconds,
    }
