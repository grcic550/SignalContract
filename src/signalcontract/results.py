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
            rules = contract.expect
            
            if not rules:
                return cls(
                    status = "FAIL",
                    reason_code = "NO_RULES_DEFINED",
                    mismatched_fields = {},
                    matched_events = []

                )
            matched_events = matcher(contract, events)

            if matched_events:
                return cls(
                    status = "PASS",
                    reason_code = "SUCCESS",
                    mismatched_fields = {},
                    matched_events = matched_events
                )
            
            target_event_type = rules.get("event_type")

            candidate_events = [
                event for event in events
                if target_event_type is None or getattr(event, "event_type", None) == target_event_type
            ]

            if not candidate_events:
                return cls(
                    status = "FAIL",
                    reason_code = "NO_MATCHING_EVENTS",
                    mismatched_fields = {},
                    matched_events = []
                )

            best_mismatches = None

            for candidate_event in candidate_events:
                current_mismatches = {}

                for field, expected_value in rules.items():
                    actual_value = getattr(candidate_event, field, None)
                    if actual_value != expected_value:
                        current_mismatches[field] = {
                            "expected": expected_value,
                            "actual": actual_value,
                        }

                if best_mismatches is None or len(current_mismatches) < len(best_mismatches):
                    best_mismatches = current_mismatches

            return cls(
                status = "FAIL",
                reason_code = "MISMATCHED_FIELDS",
                mismatched_fields = best_mismatches,
                matched_events = [],
            )
        
        except Exception as e:
            return cls(
                status = "FAIL",
                reason_code = f"ERROR: {str(e)}",
                mismatched_fields = {},
                matched_events = [],
            )
            