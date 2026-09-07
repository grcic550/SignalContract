from signalcontract.matcher import matcher
from signalcontract.models import SecurityEvent
from signalcontract.models import Contract

def test_matcher_happy_path():

    contract = Contract(
        version = 1,
        scenario = "login_success",
        expect = {
            "event_type": "login"
        }
    )

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

def test_event_satisfy_every_expectation():

    contract = Contract(
        version = 1,
        scenario = "login_success",
        expect = {
            "event_type": "authorization.denied",
            "actor": "user",
            "action": "login",
            "target": "system",
            "outcome": "denied",
            "reason": "user not authorized",
            "timestamp": "2023-10-01T12:00:00Z"
        },
    )

    event = SecurityEvent(
        event_type = "authorization.denied",
        actor = "user",
        action = "login",
        target = "system",
        outcome = "success",
        reason = "user not authorized",
        timestamp = "2023-10-01T12:00:00Z"
    )

    result = matcher(contract, [event])

    assert len(result) == 0


def test_empty_events_list_returns_empty_list():

    contract = Contract(
        version = 1,
        scenario = "login_success",
        expect = {
            "event_type": "authorization.success",
            "actor": "user",
            "action": "login",
            "target": "system",
            "outcome": "success",
            "reason": "user authenticated",
            "timestamp": "2023-10-01T12:00:00Z"
        }
    )

    events = []

    result = matcher(contract, events)

    assert len(result) == 0

def test_two_fully_matching_events_are_returned():

    contract = Contract(
        version = 1,
        scenario = "login_success",
        expect = {
            "event_type": "authorization.success",
            "actor": "user",
            "action": "login",
            "target": "system",
            "outcome": "success",
            "reason": "user authenticated",
            "timestamp": "2023-10-01T12:00:00Z"
        }
    )

    event1 = SecurityEvent(
        event_type = "authorization.success",
        actor = "user",
        action = "login",
        target = "system",
        outcome = "success",
        reason = "user authenticated",
        timestamp = "2023-10-01T12:00:00Z"
    )

    event2 = SecurityEvent(
        event_type = "authorization.success",
        actor = "user",
        action = "login",
        target = "system",
        outcome = "success",
        reason = "user authenticated",
        timestamp = "2023-10-01T12:00:00Z"
    )

    events = [event1, event2]

    result = matcher(contract, events)

    assert len(result) == 2

def test_complementary_partial_matches_are_not_returned():

    contract = Contract(
        version = 1,
        scenario = "login_success",
        expect = {
            "event_type": "authorization.success",
            "outcome": "success",
        }
    )

    event1 = SecurityEvent(
        event_type = "authorization.success",
        actor = "admin",
        action = "server_login",
        target = "server",
        outcome = "denied",
        reason = "error 403",
        timestamp = "2023-10-01T13:00:00Z"
    )

    event2 = SecurityEvent(
        event_type = "authorization.denied",
        actor = "admin",
        action = "server_login",
        target = "server",
        outcome = "success",
        reason = "successful login",
        timestamp = "2023-10-01T10:00:00Z"
    )

    events = [event1, event2]

    result = matcher(contract, events)

    assert len(result) == 0
    assert event1 not in result
    assert event2 not in result

def test_output(capsys):

    contract = Contract(
        version = 1,
        scenario = "login_success",
        expect = {
            "event_type": "authorization.success",
            "outcome": "success",
        }
    )

    event1 = SecurityEvent(
        event_type = "authorization.success",
        actor = "admin",
        action = "server_login",
        target = "server",
        outcome = "denied",
        reason = "error 403",
        timestamp = "2023-10-01T13:00:00Z"
    )

    event2 = SecurityEvent(
        event_type = "authorization.denied",
        actor = "admin",
        action = "server_login",
        target = "server",
        outcome = "success",
        reason = "successful login",
        timestamp = "2023-10-01T10:00:00Z"
    )

    events = [event1, event2]

    result = matcher(contract, events)

    assert len(result) == 0

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""

def test_silence_when_event_matches(capsys):

    contract = Contract(
        version = 1,
        scenario = "login_success",
        expect = {
            "event_type": "authorization.success",
            "outcome": "success",
        }
    )

    event = SecurityEvent(
        event_type = "authorization.success",
        actor = "admin",
        action = "server_login",
        target = "server",
        outcome = "success",
        reason = "successful login",
        timestamp = "2023-10-01T10:00:00Z"
    )

    result = matcher(contract, [event])

    assert len(result) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""