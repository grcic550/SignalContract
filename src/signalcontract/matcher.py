
from signalcontract.models import Contract


def matcher(contract: Contract, events: list):
    """Matches a list of events against the rules defined in a security contract."""

    matched_events = []

    rules = contract.expect

    if not rules:
        return matched_events  # No rules to match against

    for event in events:

        if all(hasattr(event, field) and getattr(event, field) == value for field, value in rules.items()):
            matched_events.append(event)

    return matched_events