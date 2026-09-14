from dataclasses import dataclass

from signalcontract.models import SecurityEvent


@dataclass
class VerificationResult:
    """Represents the result of verifying a security contract
    against a set of events."""

    status: str
    reason_code: str
    mismatched_fields: dict
    matched_events: list[SecurityEvent]
