import json
from signalcontract.models import SecurityEvent
from signalcontract.errors import EventParseError, ValidationError


def parse_log_file(file_path: str):

    events = []

    with open(file_path, "r") as file:

        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
                event = SecurityEvent.from_dict(data)
                events.append(event)

            except json.JSONDecodeError as e:
                raise EventParseError(f"Line number {line_number}: Malformed JSON - {str(e)}")

            except ValidationError as e:
                raise ValidationError(f"Line number {line_number}: Validation failed - {str(e)}")

    return events