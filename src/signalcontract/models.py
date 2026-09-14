from dataclasses import dataclass
from typing import Optional
from signalcontract.errors import ValidationError
from difflib import get_close_matches

@dataclass
class SecurityEvent:
    event_type: str
    actor: str
    action: str
    target: str
    outcome: str
    reason: str
    timestamp: str
    correlation_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        """Converts a raw dictionary into a type-safe SecurityEvent model.
        
        Rejects the input and raises a ValidationError if required fields are missing.
        """
        if data is None:
            raise ValidationError("Event data is None. It must be a dictionary with required fields.")
        
        if not isinstance(data, dict):
            raise ValidationError("SecurityEvent data must be a dictionary.")

        required_fields = ["event_type", "actor", "action", "target", "outcome", "reason", "timestamp"]

        for field in required_fields:
            if field not in data or not data[field]:
                raise ValidationError(f"Missing required security-event field {field}")

        return cls(
            event_type=data["event_type"],
            actor=data["actor"],
            action=data["action"],
            target=data["target"],
            outcome=data["outcome"],
            reason=data["reason"],
            timestamp=data["timestamp"],
            correlation_id=data.get("correlation_id")
        )

def check_invalid_keys(data: dict, expected_keys: list):
    invalid_keys = [k for k in data["expect"] if k not in expected_keys]
    close_matches = {k: get_close_matches(k, expected_keys) for k in invalid_keys}
    
    for k, matches in close_matches.items():
        if matches:
            raise ValidationError(f"Contract expect field contains invalid key '{k}', did you mean '{matches[0]}'?")
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
        """Converts a raw dictionary int a type-safe Contract model.
        Rejects the input and raises a ValidationError if required fields are missing."""

        required_fields = ["version", "scenario", "expect"]
        expected_keys = ["event_type", "actor", "action", "target", "outcome", "reason", "timestamp"]

        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required contract field {field}.")

        if not data["scenario"]:
            raise ValidationError("Contract scenario must not be empty.")
        
        if not isinstance(data["expect"], dict):
            raise ValidationError("Contract expect field must be a dictionary.")

        if not all(isinstance(k, str) and isinstance(v, str) for k, v in data["expect"].items()):
            raise ValidationError("Contract expect field must be a dictionary of string keys and string values.")

        if "correlation_id" not in data["expect"]:
            check_invalid_keys(data, expected_keys)
        elif "correlation_id" in data["expect"]:
            check_invalid_keys(data, expected_keys + ["correlation_id"])


        if not data["version"]:
            raise ValidationError("Contract version must be an integer and equal to 1 because only version 1 is supported.")
        
        if isinstance(data["version"], bool):
            raise ValidationError("Contract version must be an integer and equal to 1 because only version 1 is supported.")
        
        if isinstance(data["version"], int) and data["version"] == 1:
            pass
        else:
            raise ValidationError("Contract version must be an integer and equal to 1 because only version 1 is supported.")

        return cls(
            version = data["version"],
            scenario = data["scenario"],
            expect = data["expect"]
        )
        