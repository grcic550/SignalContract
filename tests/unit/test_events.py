import pytest
from signalcontract.models import SecurityEvent
from signalcontract.errors import ValidationError
from signalcontract.events import parse_log_file
from signalcontract.errors import EventParseError


def test_valid_security_event_creates_security_event():
    """Validate a security event file for correctness."""

    valid_event = {
        "event_type": "login",
        "actor": "user",
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": "2023-10-01T12:00:00Z"
    }

    result = SecurityEvent.from_dict(valid_event)

    assert result.event_type == "login"
    assert result.actor == "user"
    assert result.action == "login"
    assert result.target == "system"
    assert result.outcome == "success"
    assert result.reason == "user authenticated"
    assert result.timestamp == "2023-10-01T12:00:00Z"

def test_invalid_security_event_raises_validation_error():

    """Test that an invalid security event raises a validation error."""

    invalid_event = {
        "event_type": "login",
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": "2023-10-01T12:00:00Z"
    }

    with pytest.raises(ValidationError, match=r"Missing required security-event field actor"):
        SecurityEvent.from_dict(invalid_event)

def test_parse_log_file_with_jsonl(tmp_path):

    """Test parsing a JSONL log file."""

    log_file = tmp_path / "events.jsonl"
    log_file.write_text(
        '{"event_type": "login", "actor": "user", "action": "login", "target": "system", "outcome": "success", "reason": "user authenticated", "timestamp": "2023-10-01T12:00:00Z"}\n'
        '{"event_type": "logout", "actor": "user", "action": "logout", "target": "system", "outcome": "failure", "reason": "user failed to authenticate", "timestamp": "2023-10-01T12:00:00Z"}\n'
    )

    events = parse_log_file(str(log_file))

    assert len(events) == 2
    assert events[0].event_type == "login"
    assert events[1].event_type == "logout"

def test_parse_log_file_with_json(tmp_path):

    """Test parsing a JSON log file."""

    log_file = tmp_path / "events.json"
    log_file.write_text(
        '[{"event_type": "login", "actor": "user", "action": "login", "target": "system", "outcome": "success", "reason": "user authenticated", "timestamp": "2023-10-01T12:00:00Z"}, {"event_type": "logout", "actor": "user", "action": "logout", "target": "system", "outcome": "failure", "reason": "user failed to authenticate", "timestamp": "2023-10-01T12:00:00Z"}]'
    )

    events = parse_log_file(str(log_file))

    assert len(events) == 2
    assert events[0].event_type == "login"
    assert events[1].event_type == "logout"

def test_parse_log_file_rejects_malformed_jsonl(tmp_path):

    """Test that a malformed JSONL log file raises a ValueError."""

    log_file = tmp_path / "malformed_events.jsonl"
    log_file.write_text(
        '{"event_type": login, "actor": "user", "action": "login", "target": "system", "outcome": "success", "reason": "user authenticated", "timestamp": "2023-10-01T12:00:00Z"}\n'
        '{"event_type": "logout", "actor": "user", "action": "logout", "target": "system", "outcome": "failure", "reason": "user failed to authenticate", "timestamp": "2023-10-01T12:00:00Z"}\n'
    )

    with pytest.raises(EventParseError, match=r"Malformed JSONL line 1"):
        parse_log_file(str(log_file))

def test_parse_log_file_rejects_malformed_json(tmp_path):

    """Test that a malformed JSON log file raises a ValueError."""

    log_file = tmp_path / "malformed_events.json"
    log_file.write_text(
        '[{"event_type": login, "actor": "user", "action": "login", "target": "system", "outcome": "success", "reason": "user authenticated", "timestamp": "2023-10-01T12:00:00Z"}, {"event_type": logout, "actor": "user", "action": "logout", "target": "system", "outcome": "failure", "reason": "user failed to authenticate", "timestamp": "2023-10-01T12:00:00Z"}]'
    )

    with pytest.raises(EventParseError, match=r"Malformed JSON file"):
        parse_log_file(str(log_file))