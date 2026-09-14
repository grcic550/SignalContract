import pytest

from signalcontract.contract import load_contract
from signalcontract.errors import EventParseError, ValidationError
from signalcontract.models import Contract


def test_valid_contract_creates_contract():
    """Validate a contract file for correctness."""

    valid_contract = {
        "version": 1,
        "scenario": "denied_admin_db_deletion",
        "expect": {
            "event_type": "authorization.denied",
        },
    }

    result = Contract.from_dict(valid_contract)

    assert result.scenario == "denied_admin_db_deletion"
    assert result.expect["event_type"] == "authorization.denied"


def test_invalid_contract_raises_validation_error():

    contract = {"version": 1, "expect": {"event_type": "authorization.denied"}}

    with pytest.raises(
        ValidationError, match=r"Missing required contract field scenario\."
    ):
        Contract.from_dict(contract)


def test_missing_expect_raises_validation_error():

    contract = {"version": 1, "scenario": "denied_admin_db_deletion"}

    with pytest.raises(
        ValidationError, match=r"Missing required contract field expect\."
    ):
        Contract.from_dict(contract)


def test_empty_expect_is_accepted():

    contract = {"version": 1, "scenario": "denied_admin_db_deletion", "expect": {}}

    result = Contract.from_dict(contract)

    assert result.version == 1
    assert result.scenario == "denied_admin_db_deletion"
    assert result.expect == {}


def test_expect_not_dict_raises_validation_error():

    contract = {
        "version": 1,
        "scenario": "denied_admin_db_deletion",
        "expect": "denied",
    }

    with pytest.raises(
        ValidationError, match=r"Contract expect field must be a dictionary\."
    ):
        Contract.from_dict(contract)


def test_expect_with_non_string_keys_raises_validation_error():

    contract = {
        "version": 1,
        "scenario": "denied_admin_db_deletion",
        "expect": {1: "authorization.denied"},
    }

    with pytest.raises(
        ValidationError,
        match=r"Contract expect field must be a dictionary of "
        r"string keys and string values\.",
    ):
        Contract.from_dict(contract)


def test_expect_misspelled_key_raises_validation_error():

    contract = {
        "version": 1,
        "scenario": "denied_admin_db_deletion",
        "expect": {"outocme": "authorization.denied"},
    }

    with pytest.raises(
        ValidationError,
        match=r"Contract expect field contains invalid"
        r"key 'outocme', did you mean 'outcome'?",
    ):
        Contract.from_dict(contract)


def test_expect_contains_correlation_id_key_accepted():

    contract = {
        "version": 1,
        "scenario": "another_scenario",
        "expect": {"correlation_id": "some_correlation_id"},
    }

    result = Contract.from_dict(contract)

    assert result.scenario == "another_scenario"
    assert result.expect["correlation_id"] == "some_correlation_id"


def test_empty_yaml_file_raises_event_parse_error(tmp_path):

    empty_contract_file = tmp_path / "empty_contract.yaml"
    empty_contract_file.write_text("")

    with pytest.raises(
        EventParseError,
        match=r"Contract data is empty. It must contain a mapping of fields\.",
    ):
        load_contract(str(empty_contract_file))


def test_yaml_file_with_non_dict_content_raises_event_parse_error(tmp_path):

    non_dict_contract_file = tmp_path / "non_dict_contract.yaml"
    non_dict_contract_file.write_text("42")

    with pytest.raises(
        EventParseError,
        match=r"Contract data is not a dictionary. It must be a mapping of fields\.",
    ):
        load_contract(str(non_dict_contract_file))


def test_contract_version_out_of_range_raises_validation_error():

    contract = {
        "version": 11,
        "scenario": "denied_admin_db_deletion",
        "expect": {"event_type": "authorization.denied"},
    }

    with pytest.raises(
        ValidationError,
        match=r"Contract version must be an integer and "
        r"equal to 1 because only version 1 is supported\.",
    ):
        Contract.from_dict(contract)


def test_contract_version_not_integer_raises_validation_error():

    contract = {
        "version": "1",
        "scenario": "denied_admin_db_deletion",
        "expect": {"event_type": "authorization.denied"},
    }

    with pytest.raises(
        ValidationError,
        match=r"Contract version must be an integer and "
        r"equal to 1 because only version 1 is supported\.",
    ):
        Contract.from_dict(contract)


def test_contract_with_version_is_valid():

    contract = {
        "version": 1,
        "scenario": "denied_admin_db_deletion",
        "expect": {"event_type": "authorization.denied"},
    }

    result = Contract.from_dict(contract)

    assert result.version == 1
    assert result.scenario == "denied_admin_db_deletion"
    assert result.expect["event_type"] == "authorization.denied"

    assert len(result.expect) == 1


def test_contract_with_version_boolean_is_invalid():

    contract = {
        "version": True,
        "scenario": "denied_admin_db_deletion",
        "expect": {"event_type": "authorization.denied"},
    }

    with pytest.raises(
        ValidationError,
        match=r"Contract version must be an integer and "
        r"equal to 1 because only version 1 is supported\.",
    ):
        Contract.from_dict(contract)
