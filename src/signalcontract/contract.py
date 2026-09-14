import yaml

from signalcontract.errors import EventParseError, ValidationError
from signalcontract.models import Contract


def load_contract(file_path: str) -> Contract:
    """Loads a security contract from a YAML file and returns it as a Contract."""

    with open(file_path, encoding="utf-8") as file:
        try:
            contract_data = yaml.safe_load(file)

            if contract_data is None:
                raise EventParseError(
                    "Contract data is empty. It must contain a mapping of fields."
                )

            if isinstance(contract_data, dict) is False:
                raise EventParseError(
                    "Contract data is not a dictionary. It must be a mapping of fields."
                )

            if len(contract_data) == 0:
                raise EventParseError(
                    "Contract data is empty. It must contain a mapping of fields."
                )

            contract = Contract.from_dict(contract_data)

            return contract
        except yaml.YAMLError as e:
            raise EventParseError(f"Malformed YAML file:{e}") from e

        except ValidationError as e:
            raise EventParseError(f"Validation error in contract file: {e}") from e
