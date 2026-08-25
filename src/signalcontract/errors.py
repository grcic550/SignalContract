class SignalContractError(Exception):
    """Base exception for all SignalContract errors."""
    pass

class ValidationError(SignalContractError):
    """Raised when an event or contract fails validation due to missing or invalid fields."""
    pass

class EventParseError(SignalContractError):
    """Raised when an event cannot be parsed from a JSONL file or JSONL line is malformed."""
    pass