import pytest
from signalcontract.models import Contract
from signalcontract.errors import ValidationError

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

    contract = {
        "version": 1,
        "expect":{
            "event_type": "authorization.denied"
        }
    }

    with pytest.raises(ValidationError, match=r"Missing required contract field scenario\."):
        Contract.from_dict(contract)

def test_missing_expect_raises_validation_error():

    contract = {
        "version": 1,
        "scenario": "denied_admin_db_deletion"
    }

    with pytest.raises(ValidationError, match=r"Missing required contract field expect\."):
        Contract.from_dict(contract)

def test_empty_expect_raises_validation_error():

    contract = {
        "version": 1,
        "scenario": "denied_admin_db_deletion",
        "expect": {}
    }

    with pytest.raises(ValidationError, match=r"Missing required contract field expect\."):
        Contract.from_dict(contract)

