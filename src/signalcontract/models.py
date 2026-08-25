from dataclasses import dataclass
from typing import Optional
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
    correlation_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        """Converts a raw dictionary into a type-safe SecurityEvent model.
        
        Rejects the input and raises a ValidationError if required fields are missing.
        """

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
