import json

import pytest

from signalcontract.errors import EventParseError, ValidationError
from signalcontract.events import parse_log_file
from signalcontract.models import SecurityEvent


def test_valid_security_event_creates_security_event():
    """Validate a security event file for correctness."""

    valid_event = {
        "event_type": "login",
        "actor": "user",
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": "2023-10-01T12:00:00Z",
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
        "timestamp": "2023-10-01T12:00:00Z",
    }

    with pytest.raises(
        ValidationError, match=r"Missing required security-event field actor"
    ):
        SecurityEvent.from_dict(invalid_event)


def test_parse_log_file_with_jsonl(tmp_path):
    """Test parsing a JSONL log file."""

    log_file = tmp_path / "events.jsonl"

    event = {
        "event_type": "login",
        "actor": "user",
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": "2023-10-01T12:00:00Z",
    }
    event2 = {
        "event_type": "logout",
        "actor": "user",
        "action": "logout",
        "target": "system",
        "outcome": "failure",
        "reason": "user failed to authenticate",
        "timestamp": "2023-10-01T12:00:00Z",
    }

    log_file.write_text(
        "\n".join(
            [
                json.dumps(event),
                json.dumps(event2),
            ]
        )
        + "\n"
    )

    events = parse_log_file(str(log_file))

    assert len(events) == 2
    assert events[0].event_type == "login"
    assert events[1].event_type == "logout"


def test_parse_log_file_with_json(tmp_path):
    """Test parsing a JSON log file."""

    log_file = tmp_path / "events.json"

    event = {
        "event_type": "login",
        "actor": "user",
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": "2023-10-01T12:00:00Z",
    }
    log_file.write_text(json.dumps([event], indent=4))

    events = parse_log_file(str(log_file))

    assert len(events) == 1
    assert events[0].event_type == "login"


def test_parse_log_file_rejects_malformed_jsonl(tmp_path):
    """Test that a malformed JSONL log file raises a ValueError."""

    log_file = tmp_path / "malformed_events.jsonl"

    malformed_event = (
        '{"event_type": login, '
        '"actor": "user", '
        '"action": "login", '
        '"target": "system", '
        '"outcome": "success", '
        '"reason": "user authenticated", '
        '"timestamp": "2023-10-01T12:00:00Z"}'
    )

    valid_event = (
        '{"event_type": "logout", '
        '"actor": "user", '
        '"action": "logout", '
        '"target": "system", '
        '"outcome": "failure", '
        '"reason": "user failed to authenticate", '
        '"timestamp": "2023-10-01T12:00:00Z"}'
    )

    log_file.write_text(malformed_event + "\n" + valid_event + "\n")

    with pytest.raises(EventParseError, match=r"Malformed JSONL line 1"):
        parse_log_file(str(log_file))


def test_parse_log_file_rejects_malformed_json(tmp_path):
    """Test that a malformed JSON log file raises a ValueError."""

    log_file = tmp_path / "malformed_events.json"

    event = {
        "event_type": "login",
        "actor": "user",
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": "2023-10-01T12:00:00Z",
    }

    log_file.write_text(
        json.dumps([event], indent=4)[
            :-1
        ]  # Remove the closing bracket to make it malformed
    )

    with pytest.raises(EventParseError, match=r"Malformed JSON file"):
        parse_log_file(str(log_file))


def test_event_file_contains_private_fields_in_jsonl(tmp_path):
    """Test that a log file containing private fields
    raises an EventParseError."""

    log_file = tmp_path / "private_fields.jsonl"

    event_with_private_field = {
        "event_type": "login",
        "actor": "user",
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": "2023-10-01T12:00:00Z",
        "password": "p@ssw0rd",
    }

    log_file.write_text(json.dumps(event_with_private_field) + "\n")

    with pytest.raises(
        EventParseError,
        match=r"Private fields detected in the JSONL "
        "line 1. Please ensure that sensitive "
        "data is not included in the log file.",
    ) as error:
        parse_log_file(str(log_file))

    assert "Private fields detected in the JSONL line 1" in str(error.value)
    assert "Please ensure that sensitive data is not included in the log file." in str(
        error.value
    )
    assert "password" not in str(error.value)
    assert "p@ssw0rd" not in str(error.value)


def test_event_file_contains_private_fields_in_json(tmp_path):

    log_file = tmp_path / "private_fields.json"

    event_with_private_field = {
        "event_type": "login",
        "actor": "user",
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": "2023-10-01T12:00:00Z",
        "password": "p@ssw0rd",
    }

    log_file.write_text(json.dumps([event_with_private_field], indent=4))

    with pytest.raises(
        EventParseError,
        match=r"Private fields detected in the JSON event "
        "at index 1. Please ensure that sensitive data "
        "is not included in the log file.",
    ) as error:
        parse_log_file(str(log_file))

    assert "Private fields detected in the JSON event at index 1" in str(error.value)
    assert "Please ensure that sensitive data is not included in the log file." in str(
        error.value
    )
    assert "password" not in str(error.value)
    assert "p@ssw0rd" not in str(error.value)


def test_event_with_non_string_fields_raises_validation_error():
    """Test that an event with non-string
    fields raises a ValidationError."""

    invalid_event = {
        "event_type": "login",
        "actor": "user",
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": 1234567890,  # Invalid type: should be a string
    }

    with pytest.raises(
        ValidationError,
        match=r"SecurityEvent field timestamp must be a string and "
        "not None. Received type: <class 'int'>",
    ) as error:
        SecurityEvent.from_dict(invalid_event)

    assert (
        "SecurityEvent field timestamp must be a string and "
        "not None. Received type: <class 'int'>" in str(error.value)
    )


def test_event_with_correlation_id_non_string_raises_validation_error():
    """Test that an event with a non-string correlation_id
    waises an ValidationError."""

    invalid_event = {
        "event_type": "login",
        "actor": "user",
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": "2023-10-01T12:00:00Z",
        "correlation_id": 1234567890,  # Invalid type: should be a string
    }

    with pytest.raises(
        ValidationError,
        match=r"SecurityEvent field correlation_id must be a string and "
        "not None. Received type: <class 'int'>",
    ) as error:
        SecurityEvent.from_dict(invalid_event)

    assert (
        "SecurityEvent field correlation_id must be a string and "
        "not None. Received type: <class 'int'>" in str(error.value)
    )


def test_event_with_correlation_id_empty_string_raises_validation_error():
    """Test that an event with an empty string correlation_id
    raises a ValidationError."""

    invalid_event = {
        "event_type": "login",
        "actor": "user",
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": "2023-10-01T12:00:00Z",
        "correlation_id": "",  # Invalid: empty string
    }

    with pytest.raises(
        ValidationError,
        match=r"SecurityEvent field correlation_id must not "
        "be an empty string.",
    ) as error:
        SecurityEvent.from_dict(invalid_event)

    assert "SecurityEvent field correlation_id must not be an empty string." in str(
        error.value
    )


def test_event_with_empty_string_field_raises_ValidationError():
    """Test that an event with an empty string field
    raises a ValidationError."""

    invalid_event = {
        "event_type": "login",
        "actor": "user",
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": " ",  # Invalid: empty string
        "timestamp": "2023-10-01T12:00:00Z",
    }

    with pytest.raises(
        ValidationError,
        match=r"SecurityEvent field reason must not be an empty string.",
    ) as error:
        SecurityEvent.from_dict(invalid_event)

    assert "SecurityEvent field reason must not be an empty string." in str(error.value)


def test_event_with_none_field_raises_validation_error():
    """Test that an event with a None field
    raises a Validation Error."""

    invalid_event = {
        "event_type": "login",
        "actor": None,
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": "2023-10-01T12:00:00Z",
    }

    with pytest.raises(
        ValidationError,
        match=r"Missing required security-event field actor",
    ) as error:
        SecurityEvent.from_dict(invalid_event)

    assert "Missing required security-event field actor" in str(error.value)


def test_event_jsonl_file_with_field_with_none_raises_EventParseError(tmp_path):
    """Test that a log file containing a field with None
    raises an EventParseError."""

    log_file = tmp_path / "none_field.jsonl"

    event_with_good_fields = {
        "event_type": "login",
        "actor": "user",
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": "2023-10-01T12:00:00Z",
    }

    event_with_none_field = {
        "event_type": "login",
        "actor": None,
        "action": "login",
        "target": "system",
        "outcome": "success",
        "reason": "user authenticated",
        "timestamp": "2023-10-01T12:00:00Z",
    }

    log_file.write_text(
        json.dumps(event_with_good_fields)
        + "\n"
        + json.dumps(event_with_none_field)
        + "\n"
    )

    with pytest.raises(
        EventParseError,
        match=r"Validation error in JSONL line 2: "
        "Missing required security-event field actor",
    ) as error:
        parse_log_file(str(log_file))

    assert (
        "Validation error in JSONL line 2: "
        "Missing required security-event field actor" in str(error.value)
    )
