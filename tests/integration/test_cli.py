import json
from pathlib import Path

import pytest
import yaml
from typer.testing import CliRunner

from signalcontract.cli import app


def test_valid_contract_exit_sucessfully():
    """Test that the validate function exits sucessfully with a
    valid contract file."""

    runner = CliRunner()
    result = runner.invoke(
        app, ["validate", "--contract", "tests/fixtures/valid-contract.yaml"]
    )

    assert result.exit_code == 0


def test_validate_rejects_contract_without_scenario():
    """Test that the validate function exits sucessfully with error."""

    runner = CliRunner()
    result = runner.invoke(
        app, ["validate", "--contract", "tests/fixtures/invalid-contract.yaml"]
    )

    assert result.exit_code == 1
    assert "Error: Validation error in contract file:" in result.output
    assert "Missing required contract field scenario." in result.output


def test_verify_passes_when_an_event_matches():
    """Test that the verify function exits successfully when an
    event matches the contract."""

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "verify",
            "--contract",
            "tests/fixtures/valid-contract.yaml",
            "--events",
            "tests/fixtures/valid-events.json",
        ],
    )

    assert result.exit_code == 0
    assert "PASS: matched 1 event(s)." in result.output


def test_verify_rejects_malformed_events_file():
    """Test that the verify function exits with error when
    the events file is malformed."""

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "verify",
            "--contract",
            "tests/fixtures/valid-contract.yaml",
            "--events",
            "tests/fixtures/invalid-events.jsonl",
        ],
    )

    assert result.exit_code == 1
    assert "Error: Malformed JSONL line 2:" in result.output


def test_verify_no_events_file_raises_error():

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["verify", "--contract", "tests/fixtures/valid-contract.yaml", "--events", ""],
    )

    assert result.exit_code == 1
    assert "Error: No events file provided." in result.output


def test_verify_no_contract_file_raises_error():

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["verify", "--contract", "", "--events", "tests/fixtures/valid-events.json"],
    )

    assert result.exit_code == 1
    assert "Error: No contract file provided." in result.output


def test_verify_no_file_provided_raises_error():

    runner = CliRunner()
    result = runner.invoke(app, ["verify", "--contract", "", "--events", ""])

    assert result.exit_code == 1
    assert "Error: No contract or events file provided." in result.output


def test_verify_no_file_error(tmp_path):
    """Test that the verify function exits with error when a file is not found."""

    missing_contract_file = tmp_path / "missing_contract.yaml"

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "verify",
            "--contract",
            str(missing_contract_file),
            "--events",
            "tests/fixtures/valid-events.json",
        ],
    )

    assert result.exit_code == 1
    assert "Error: File not found: " in result.output
    assert str(missing_contract_file) in result.output


def test_verify_no_events_file_error(tmp_path):

    missing_events_file = tmp_path / "missing_events.json"

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "verify",
            "--contract",
            "tests/fixtures/valid-contract.yaml",
            "--events",
            str(missing_events_file),
        ],
    )

    assert result.exit_code == 1
    assert "Error: File not found: " in result.output
    assert str(missing_events_file) in result.output


def test_verify_mismatched_fields():
    """Test that the verify function exits with an
    error when an event has mismatched fields."""

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "verify",
            "--contract",
            "tests/fixtures/valid-contract.yaml",
            "--events",
            "tests/fixtures/mismatched-events.json",
        ],
    )

    assert result.exit_code == 1
    assert "FAIL: MISMATCHED_FIELDS" in result.output
    assert "Mismatched Fields:" in result.output
    assert "Field: outcome" in result.output


def test_verify_matched_fields():

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "verify",
            "--contract",
            "tests/fixtures/valid-contract.yaml",
            "--events",
            "tests/fixtures/valid-events.json",
        ],
    )

    assert result.exit_code == 0
    assert "PASS: matched 1 event(s)." in result.output
    assert "Match 1:" in result.output
    assert "Event Type: authorization.denied" in result.output
    assert "Actor: user-42" in result.output
    assert "Action: delete_database" in result.output
    assert "Target: prod_db" in result.output
    assert "Reason: insufficient_privileges" in result.output
    assert "Timestamp: 2026-08-25T12:01:15Z" in result.output


def test_verify_no_matching_events():
    """Test that the verify function exits with an error
    when no event matches the contract."""

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "verify",
            "--contract",
            "tests/fixtures/valid-contract.yaml",
            "--events",
            "tests/fixtures/unmatched-events.jsonl",
        ],
    )

    assert result.exit_code == 1
    assert "FAIL: NO_MATCHING_EVENTS" in result.output


def test_verify_no_rules_defined():
    """Test that the verify function exits with an error
    when no rules are defined in the contract."""

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "verify",
            "--contract",
            "tests/fixtures/no-rules-contract.yaml",
            "--events",
            "tests/fixtures/valid-events.json",
        ],
    )

    assert result.exit_code == 1
    assert "FAIL: NO_RULES_DEFINED" in result.output


def test_verify_private_fields_in_event_jsonl_file_throw_an_error():
    """Test that the verify function exits with an error
    when a JSONL event file contains private fields."""

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "verify",
            "--contract",
            "tests/fixtures/valid-contract.yaml",
            "--events",
            "tests/fixtures/events-with-private-fields.jsonl",
        ],
    )

    assert result.exit_code == 1
    assert "Error: Private fields detected in the JSONL line 2." in result.output
    assert (
        "Please ensure that sensitive "
        "data is not included in the log file." in result.output
    )
    assert "SYNTHETIC_TEST_PASSWORD" not in result.output


def test_verify_private_fields_in_event_json_file_throw_an_error():
    """Test that the verify function exits with an error
    when a JSON event file contains private fields."""

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "verify",
            "--contract",
            "tests/fixtures/valid-contract.yaml",
            "--events",
            "tests/fixtures/events-with-private-fields.json",
        ],
    )

    assert result.exit_code == 1
    assert (
        "Error: Private fields detected in the JSON event at index 2." in result.output
    )
    assert (
        "Please ensure that sensitive "
        "data is not included in the log file." in result.output
    )
    assert "SYNTHETIC_TEST_PASSWORD" not in result.output


@pytest.mark.parametrize("correlation_id", ["", "   ", "\t"])
def test_verify_blank_correlation_id_raises_error(correlation_id):
    """Test that the verify function exits with an error
    when an empty correlation_id is provided."""

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "verify",
            "--contract",
            "tests/fixtures/valid-contract.yaml",
            "--events",
            "tests/fixtures/valid-events.json",
            "--correlation-id",
            correlation_id,
        ],
    )

    assert result.exit_code == 1
    assert (
        "Error: correlation_id must be a non-empty string if provided." in result.output
    )
    assert "PASS" not in result.output


@pytest.mark.parametrize(
    ("contract_id", "cli_id", "expected_exit_code"),
    [
        (None, None, 0),
        ("12345", None, 0),
        ("other-request", None, 1),
        (None, "12345", 0),
        ("other-request", "12345", 0),
        ("12345", "missing-request", 1),
    ],
)
def test_verify_correlation_id_selection(
    tmp_path, contract_id, cli_id, expected_exit_code
):
    """Select one request without changing the saved contract."""
    contract_data = yaml.safe_load(
        Path("tests/fixtures/valid-contract.yaml").read_text(encoding="utf-8")
    )
    if contract_id is not None:
        contract_data["expect"]["correlation_id"] = contract_id
    contract_file = tmp_path / "contract.yaml"
    contract_file.write_text(yaml.safe_dump(contract_data), encoding="utf-8")
    original_contract = contract_file.read_bytes()

    events = json.loads(
        Path("tests/fixtures/valid-events.json").read_text(encoding="utf-8")
    )
    for event in events:
        event["correlation_id"] = "12345"
    events_file = tmp_path / "events.json"
    events_file.write_text(json.dumps(events), encoding="utf-8")

    arguments = [
        "verify",
        "--contract",
        str(contract_file),
        "--events",
        str(events_file),
    ]
    if cli_id is not None:
        arguments.extend(["--correlation-id", cli_id])

    result = CliRunner().invoke(app, arguments)

    assert result.exit_code == expected_exit_code, result.output
    if expected_exit_code == 0:
        assert "PASS: matched 1 event(s)." in result.output
    else:
        assert "FAIL: MISMATCHED_FIELDS" in result.output
        assert "Field: correlation_id" in result.output
        assert "PASS" not in result.output
    assert contract_file.read_bytes() == original_contract
