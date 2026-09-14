from signalcontract.models import Contract, SecurityEvent
from signalcontract.results import VerificationResult

def verify_contract(contract: Contract, events: list[SecurityEvent]) -> VerificationResult:

    """Verifies a contract against a list of events and returns
    the verification result."""

    return VerificationResult.from_matcher(contract, events)