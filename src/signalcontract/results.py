from signalcontract.matcher import matcher
from dataclasses import dataclass

@dataclass
class VerificationResult:
    """Represents the result of verifying a security contract against a set of events."""

    status: str
    reason_code: str
    mismatched_fields: dict
    matched_events: list


    @classmethod
    def from_matcher(cls, contract, events):
        """Creates a VerificationResult from the matcher function."""

        try:
            matched_events = matcher(contract, events)
            if matched_events:
                return cls(
                    status = "PASS",
                    reason_code = "SUCCESS",
                    mismatched_fields = {},
                    matched_events = matched_events
                )
            rules = contract.expect
            if not rules:
                return cls(
                    status = "FAIL",
                    reason_code = "NO_RULES_DEFINED",
                    mismatched_fields = {},
                    matched_events = []
                )
            target_event_type = rules.get("event_type")
            candidate_events = [
                event for event in events
                if target_event_type is None or getattr(event, "event_type", None) == target_event_type
            ]

            mismatched_fields = {}

            if not candidate_events:
                reason_code = "NO_MATCHING_EVENTS"
            else:
                reason_code = "MISMATCHED_FIELDS"
                for candidate_event in candidate_events:
                    for field, expected_value in rules.items():
                        actual_value = getattr(candidate_event, field, None)
                        if actual_value != expected_value:
                            mismatched_fields[field] = {
                                "expected": expected_value,
                                "actual": actual_value,
                            }

            return cls(
                status = "FAIL",
                reason_code = reason_code,
                mismatched_fields = mismatched_fields,
                matched_events = [],
            )
        except Exception as e:
            return cls(
                status = "FAIL",
                reason_code = f"ERROR: {str(e)}",
                mismatched_fields = {},
                matched_events = [],
            )
            