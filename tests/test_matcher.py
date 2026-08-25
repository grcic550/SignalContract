from signalcontract.matcher import matcher
from signalcontract.models import SecurityEvent

def test_matcher_happy_path():

    contract = {
        "expect":{
            "event_type": "login",
            "outcome": "success"
        }
    }

    matching_event = SecurityEvent(
        event_type = "login",
        actor = "user",
        action = "login",
        target = "system",
        outcome = "success",
        reason = "user authenticated",
        timestamp = "2023-10-01T12:00:00Z"
    )

    different_event = SecurityEvent(
        event_type = "logout",
        actor = "user",
        action = "logout",
        target = "system",
        outcome = "failure",
        reason = "user failed to authenticate",
        timestamp = "2023-10-01T12:00:00Z"
    )

    events = [matching_event, different_event]

    result = matcher(contract, events)

    assert len(result) == 1
    assert result[0] == matching_event