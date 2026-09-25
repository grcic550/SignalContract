from dataclasses import dataclass
from difflib import get_close_matches

from signalcontract.errors import ValidationError


@dataclass
class SecurityEvent:
    event_type: str
    actor: str
    action: str
    target: str
    outcome: str
    reason: str
    timestamp: str
    correlation_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict):
        """Converts a raw dictionary into a type-safe SecurityEvent model.

        Rejects the input and raises a ValidationError if required fields are missing.
        """
        if data is None:
            raise ValidationError(
                "Event data is None. It must be a dictionary with required fields."
            )

        if not isinstance(data, dict):
            raise ValidationError("SecurityEvent data must be a dictionary.")

        required_fields = [
            "event_type",
            "actor",
            "action",
            "target",
            "outcome",
            "reason",
            "timestamp",
        ]

        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValidationError(f"Missing required security-event field {field}")

            if not isinstance(data[field], str):
                raise ValidationError(
                    f"SecurityEvent field {field} must be a string and "
                    f"not None. Received type: {type(data[field])}"
                )
            if isinstance(data[field], str) and not data[field].strip():
                raise ValidationError(
                    f"SecurityEvent field {field} must not be an empty string."
                )

        if "correlation_id" in data and data["correlation_id"] is not None:
            if not isinstance(data["correlation_id"], str):
                raise ValidationError(
                    f"SecurityEvent field correlation_id must be a string and "
                    f"not None. Received type: {type(data['correlation_id'])}"
                )
            if (
                isinstance(data["correlation_id"], str)
                and not data["correlation_id"].strip()
            ):
                raise ValidationError(
                    "SecurityEvent field correlation_id must not be an empty string."
                )
        return cls(
            event_type=data["event_type"],
            actor=data["actor"],
            action=data["action"],
            target=data["target"],
            outcome=data["outcome"],
            reason=data["reason"],
            timestamp=data["timestamp"],
            correlation_id=data.get("correlation_id"),
        )


def check_invalid_keys(data: dict, expected_keys: list):
    invalid_keys = [k for k in data["expect"] if k not in expected_keys]
    close_matches = {k: get_close_matches(k, expected_keys) for k in invalid_keys}

    for k, matches in close_matches.items():
        if matches:
            raise ValidationError(
                f"Contract expect field contains invalid"
                f"key '{k}', did you mean '{matches[0]}'?"
            )
        else:
            raise ValidationError(f"Contract expect field contains invalid key '{k}'.")


@dataclass
class Contract:
    """Respresents a security contract with its associated metadata and events."""

    version: int
    scenario: str
    expect: dict[str, str]

    @classmethod
    def from_dict(cls, data: dict):
        """Converts a raw dictionary int a type-safe
        Contract model.Rejects the input and raises a
        ValidationError if required fields are missing."""

        required_fields = ["version", "scenario", "expect"]
        expected_keys = [
            "event_type",
            "actor",
            "action",
            "target",
            "outcome",
            "reason",
            "timestamp",
        ]

        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required contract field {field}.")

        if not data["scenario"]:
            raise ValidationError("Contract scenario must not be empty.")

        if not isinstance(data["expect"], dict):
            raise ValidationError("Contract expect field must be a dictionary.")

        if not all(
            isinstance(k, str) and isinstance(v, str) for k, v in data["expect"].items()
        ):
            raise ValidationError(
                "Contract expect field must be a "
                "dictionary of string keys and string values."
            )

        if "correlation_id" not in data["expect"]:
            check_invalid_keys(data, expected_keys)
        elif "correlation_id" in data["expect"]:
            check_invalid_keys(data, expected_keys + ["correlation_id"])

        if not data["version"]:
            raise ValidationError(
                "Contract version must be an integer and equal "
                "to 1 because only version 1 is supported."
            )

        if isinstance(data["version"], bool):
            raise ValidationError(
                "Contract version must be an integer and equal "
                "to 1 because only version 1 is supported."
            )

        if isinstance(data["version"], int) and data["version"] == 1:
            pass
        else:
            raise ValidationError(
                "Contract version must be an integer and equal "
                "to 1 because only version 1 is supported."
            )

        return cls(
            version=data["version"], scenario=data["scenario"], expect=data["expect"]
        )


@dataclass
class Scenario:
    """Represents a test scenario with its associated
    metadata and events."""

    version: int
    name: str
    request_method: str
    request_path: str
    expected_status: int
    contract_path: str

    @classmethod
    def from_dict(cls, data: dict):
        """Converts a raw dictionary into a type-safe
        Scenario model. Rejects the input and raises a
        ValidationError if required fields are missing."""

        required_fields = [
            "version",
            "name",
            "request",
            "expected_status",
            "contract",
        ]

        if not isinstance(data, dict):
            raise ValidationError(
                f"Scenario data must be a dictionary, but got {type(data)}"
            )

        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required scenario field {field}.")

            if not data[field]:
                raise ValidationError(f"Scenario field {field} must not be empty.")

        if not isinstance(data["request"], dict):
            raise ValidationError(
                f"Scenario request field must be a dictionary, "
                f"but got {type(data['request'])}"
            )
        elif isinstance(data["request"], dict):
            if "method" not in data["request"]:
                raise ValidationError(
                    "Missing required scenario request field 'method'."
                )
            if "path" not in data["request"]:
                raise ValidationError("Missing required scenario request field 'path'.")

        if (
            not isinstance(data["version"], (int, float))
            or data["version"] != 1.0
            or isinstance(data["version"], bool)
        ):
            raise ValidationError(
                "Scenario version must be an integer and equal "
                "to 1 because only version 1 is supported."
            )

        if data["request"]["method"] not in [
            "GET",
            "POST",
            "DELETE",
            "PUT",
            "PATCH",
            "HEAD",
            "OPTIONS",
        ]:
            raise ValidationError(
                f"Scenario request -> method must be one of "
                f"['GET', 'POST', 'DELETE', 'PUT', 'PATCH', 'HEAD', 'OPTIONS'], "
                f"but got {data['request']['method']} "
            )

        if isinstance(data["request"]["path"], str):
            if not data["request"]["path"].startswith("/"):
                raise ValidationError(
                    f"Scenario request -> path must start with a forward slash '/', "
                    f"but got {data['request']['path']}"
                )

        elif not isinstance(data["request"]["path"], str):
            raise ValidationError(
                f"Scenario request -> path must be a string, "
                f"but got {type(data['request']['path'])}"
            )

        if (
            isinstance(data["expected_status"], bool)
            or not isinstance(data["expected_status"], int)
            or not (100 <= data["expected_status"] <= 599)
        ):
            raise ValidationError(
                f"Scenario expected_status must be an integer "
                f"between 100 and 599, but got {data['expected_status']}"
            )

        return cls(
            version=data["version"],
            name=data["name"],
            request_method=data["request"]["method"],
            request_path=data["request"]["path"],
            expected_status=data["expected_status"],
            contract_path=data["contract"],
        )
