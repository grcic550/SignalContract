from signalcontract.models import Contract
from signalcontract.verify import verify_contract


def test_verify_contract_returns_error_when_matcher_raises(monkeypatch):
    """Test that verify_contract returns a VerificationResult
    when the matcher function raises an exception."""

    def broken_matcher(contract, events):
        raise RuntimeError("Something went wrong.")

    monkeypatch.setattr("signalcontract.verify.matcher", broken_matcher)

    contract = Contract(
        version=1,
        scenario="test_scenario",
        expect={"event_type": "authorization.denied"},
    )

    result = verify_contract(contract, [])

    assert result.status == "FAIL"
    assert result.reason_code == "ERROR: Something went wrong."
    assert result.mismatched_fields == {}
    assert result.matched_events == []
