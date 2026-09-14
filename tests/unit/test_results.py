from signalcontract.models import Contract
from signalcontract.results import VerificationResult

def test_from_matcher_returns_error_when_matcher_raises(monkeypatch):

    """Test that from_matcher returns a VerificationResult
    with status 'FAIL' when the matcher function raises and exception."""

    def broken_matcher(contract, events):
        raise RuntimeError("Something went wrong.")

    monkeypatch.setattr(
        "signalcontract.results.matcher",
        broken_matcher
    )

    contract = Contract(
        version = 1,
        scenario = "test_scenario",
        expect = {
            "event_type": "authorization.denied"
        }
    )

    result = VerificationResult.from_matcher(contract, [])

    assert result.status == "FAIL"
    assert result.reason_code == "ERROR: Something went wrong."
    assert result.mismatched_fields == {}
    assert result.matched_events == []