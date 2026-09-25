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


@dataclass
class RunResult:
    """Represents the result of running a test
    against a contract and a set of events."""

    scenario_name: str
    expected_status: int
    actual_status: int | None
    correlation_id: str | None
    verification: VerificationResult | None
    error_code: str | None
    status: str
