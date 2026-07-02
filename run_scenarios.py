import importlib
import sys
from colorama import Fore
import logging

logger = logging.getLogger(__name__)

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

FLOW_MODULES = [
    "configs.create_user",
    "configs.create_product_flow",
    #"configs.create_education_flow",
    "configs.promotion_product_flow",
    #"configs.promotion_education_flow"
    
]


def get_scenario_runner(*, scenario: str, scenario_runners: dict):
    try:
        scenario_config = scenario_runners[scenario]
    except KeyError as exc:
        raise KeyError(f"Unknown scenario: {scenario}") from exc

    runner_module = importlib.import_module(scenario_config["runner_module"])
    return getattr(runner_module, scenario_config["runner_function"])


def run_flow_module(module_name: str):
    flow_module = importlib.import_module(module_name)
    run_configs = getattr(flow_module, "RUN_CONFIGS")
    scenario_runners = getattr(flow_module, "SCENARIO_RUNNERS")


    logger.info(
        Fore.BLUE
        + f"\n=== Run flow module='{module_name}' ===",
    )

    for run_config in run_configs:
        scenario = run_config["scenario"]
        data_set = run_config.get("data_set")
        scenario_data = run_config.get("scenario_data")

        if data_set is not None:
            print(f"\n=== Run scenario='{scenario}' with data_set='{data_set}' ===")

        runner = get_scenario_runner(
            scenario=scenario,
            scenario_runners=scenario_runners,
        )
        if scenario_data is not None:
            runner(scenario_data=scenario_data)
        else:
            runner(data_set=data_set)


def main() -> int:
    for module_name in FLOW_MODULES:
        run_flow_module(module_name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
