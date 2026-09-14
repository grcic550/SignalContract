from signalcontract.models import Contract


def matcher(contract: Contract, events: list):
    """Matches a list of events against the rules defined in a security contract."""

    matched_events = []

    rules = contract.expect

    if not rules:
        raise ValueError("Contract has no rules defined for matching.")

    for event in events:
        if all(
            hasattr(event, field) and getattr(event, field) == value
            for field, value in rules.items()
        ):
            matched_events.append(event)

        for field in rules:
            if not hasattr(event, field):
                raise ValueError(
                    f"Fail: expected event missing required field "
                    f"'{field}' for contract matching."
                )

    return matched_events
