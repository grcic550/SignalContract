
def matcher(contract: dict, events: list):
    """Matches a list of SecurityEvent objects against a contract 
    dictionary and returns a list of matched events."""

    matched_events = []

    rules = contract.get("expect", {})

    if not rules:
        return matched_events  # No rules to match against

    for event in events:

        if all(hasattr(event, field) and getattr(event, field) == value for field, value in rules.items()):
            matched_events.append(event)

    return matched_events