import pytest
from signalcontract.cli import app
from typer.testing import CliRunner


def test_valid_contract_exit_sucessfully():

    """Test that the validate function exits sucessfully with a 
    valid contract file."""

    runner = CliRunner()
    result = runner.invoke(app, ["validate", "--contract", "tests/fixtures/valid-contract.yaml"])

    assert result.exit_code == 0

def test_validate_rejects_contract_without_scenario():

    """Test that the validate function exits sucessfully with error."""

    runner = CliRunner()
    result = runner.invoke(app, ["validate", "--contract", "tests/fixtures/invalid-contract.yaml"])

    assert result.exit_code == 1
    assert "Error: Validation error in contract file:" in result.output
    assert "Missing required contract field scenario." in result.output

def test_verify_passes_when_an_event_matches():

    """Test that the verify function exits successfully when an 
    event matches the contract."""

    runner = CliRunner()
    result = runner.invoke(app,["verify", "--contract", "tests/fixtures/valid-contract.yaml", "--events", "tests/fixtures/valid-events.json"])

    assert result.exit_code == 0
    assert "PASS: matched 1 event(s)." in result.output

def test_verify_fails_when_no_event_matches():

    """Test that the verify function exits with error when no
    event matches the contract."""

    runner = CliRunner()
    result = runner.invoke(app, ["verify", "--contract", "tests/fixtures/valid-contract.yaml", "--events", "tests/fixtures/unmatched-events.jsonl"])

    assert result.exit_code == 1
    assert "FAIL: No events matched the contract." in result.output

def test_verify_rejects_malformed_events_file():

    """Test that the verify function exits with error when
    the events file is malformed."""

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "verify",
            "--contract","tests/fixtures/valid-contract.yaml",
            "--events", "tests/fixtures/invalid-events.jsonl"
        ],
    )

    assert result.exit_code == 1
    assert "Error: Malformed JSONL line 2:" in result.output
    
    