from pathlib import Path

import yaml

from signalcontract.errors import SignalContractError
from signalcontract.models import Scenario


def load_scenario(scenario_filename: str):
    """Load a scenario from a YAML file."""

    if isinstance(scenario_filename, str):
        scenario_filename = scenario_filename.strip()
    else:
        raise TypeError("Scenario filename must be a string.")

    scenario_path = Path(scenario_filename)

    if not scenario_path.exists():
        raise FileNotFoundError(f"Scenario file not found: {scenario_filename}")

    try:
        with open(scenario_filename, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            raise SignalContractError(
                f"Scenario file {scenario_filename} must contain a YAML "
                f"mapping (dictionary) at the top level."
            )

        if not isinstance(data["request"], dict):
            raise SignalContractError(
                f"Scenario file {scenario_filename} must contain a YAML mapping "
                f"(dictionary) for the 'request' field."
            )

        scenario = Scenario.from_dict(data)

        new_contract_path = (
            scenario_path.resolve().parent.joinpath(scenario.contract_path).resolve()
        )
        scenario.contract_path = str(new_contract_path)
        return scenario

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Scenario file notfound: {scenario_filename}"
        ) from None

    except yaml.YAMLError as e:
        raise ValueError(
            f"Error parsing scenario YAML file {scenario_filename}: {e}"
        ) from None
    except Exception as e:
        raise SignalContractError(
            f"Unexpected error while loading scenario file {scenario_filename}: {e}"
        ) from None
