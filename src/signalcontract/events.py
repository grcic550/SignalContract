import json
from pathlib import Path
from signalcontract.models import SecurityEvent
from signalcontract.errors import EventParseError, ValidationError


def parse_log_file(file_path: str):

    extension = Path(file_path).suffix.lower()

    if extension == ".jsonl":
        return parse_jsonl_file(file_path)
    
    elif extension == ".json":
        return parse_json_file(file_path)

    else:
        raise EventParseError(f"Unsupported file extension: {extension}. Supported extensions are .jsonl and .json.")
        

def parse_jsonl_file(file_path: str):

    events = []

    with open(file_path, "r", encoding = "utf-8") as file:

        for line_number, line in enumerate(file, start = 1):

            line = line.strip()

            if not line:
                continue

            try:
                event_data = json.loads(line)
                if not isinstance(event_data, dict):
                    raise EventParseError(f"JSONL line {line_number} does not contain a valid JSON object.")
                event = SecurityEvent.from_dict(event_data)
                events.append(event)
            except json.JSONDecodeError as e:
                raise EventParseError(f"Malformed JSONL line {line_number}: {e}")
            except ValidationError as e:
                raise EventParseError(f"Validation error in JSONL line {line_number}: {e}")

    return events


def parse_json_file(file_path: str):

    events = []

    with open(file_path, "r", encoding = "utf-8") as file:

        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise EventParseError(f"Malformed JSON file: {e}")

        if not isinstance(data, list):
            raise EventParseError("JSON file must contain an array of events.")

        for index, event_data in enumerate(data, start = 1):
            if not isinstance(event_data, dict):
                raise EventParseError(f"JSON event at index {index} does not contain a valid JSON object.")
            try:
                event = SecurityEvent.from_dict(event_data)
                events.append(event)
            except ValidationError as e:
                raise EventParseError(f"Validation error in JSON event at index {index}: {e}")

    return events