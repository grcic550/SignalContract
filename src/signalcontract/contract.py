import yaml

def parse_yaml(file_path: str):
    """Parses a YAML file and returns its contents as a Python dictionary."""

    with open(file_path, "r",encoding = "utf-8") as file:

        contract_data = yaml.safe_load(file)

    return contract_data

