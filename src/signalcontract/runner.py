from copy import deepcopy

import httpx

from signalcontract.contract import load_contract
from signalcontract.events import parse_log_file
from signalcontract.results import RunResult
from signalcontract.verify import verify_contract


def runner(
    url: str,
    request_method: str,
    request_path: str,
    expected_status_code: int,
    contract_path: str,
    event_log_path: str,
):
    """Run a test against a contract and return the result."""

    try:
        contract = load_contract(contract_path)

    except Exception:
        return RunResult(
            scenario_name="Unknown",
            expected_status=expected_status_code,
            actual_status=None,
            correlation_id=None,
            verification=None,
            error_code="CONTRACT_LOAD_FAILED",
            status="FAIL",
        )
    # Make the request
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.request(
                method=request_method,
                url=f"{url}{request_path}",
            )
            correlation_header = response.headers.get("X-Correlation-ID")
    except httpx.RequestError:
        return RunResult(
            scenario_name=contract.scenario,
            expected_status=expected_status_code,
            actual_status=None,
            correlation_id=None,
            verification=None,
            error_code="REQUEST_FAILED",
            status="ERROR",
        )

    if correlation_header is None:
        return RunResult(
            scenario_name=contract.scenario,
            expected_status=expected_status_code,
            actual_status=response.status_code,
            correlation_id=None,
            verification=None,
            error_code="MISSING_CORRELATION_ID",
            status="ERROR",
        )

    if len(correlation_header.strip()) == 0:
        return RunResult(
            scenario_name=contract.scenario,
            expected_status=expected_status_code,
            actual_status=response.status_code,
            correlation_id=None,
            verification=None,
            error_code="EMPTY_CORRELATION_ID",
            status="ERROR",
        )
    # Check the response status code

    if response.status_code != expected_status_code:
        return RunResult(
            scenario_name=contract.scenario,
            expected_status=expected_status_code,
            actual_status=response.status_code,
            correlation_id=correlation_header,
            verification=None,
            error_code="UNEXPECTED_STATUS_CODE",
            status="FAIL",
        )

    contract_copy = deepcopy(contract)
    contract_expect = contract_copy.expect
    contract_expect["correlation_id"] = correlation_header

    # Load the events
    try:
        events = parse_log_file(event_log_path)

        verification_result = verify_contract(contract_copy, events)

        if verification_result.status == "PASS":
            run_result = RunResult(
                scenario_name=contract.scenario,
                expected_status=expected_status_code,
                actual_status=response.status_code,
                correlation_id=correlation_header,
                verification=verification_result,
                error_code=None,
                status="PASS",
            )
        else:
            run_result = RunResult(
                scenario_name=contract.scenario,
                expected_status=expected_status_code,
                actual_status=response.status_code,
                correlation_id=correlation_header,
                verification=verification_result,
                error_code="VERIFICATION_FAILED",
                status="FAIL",
            )

    except Exception:
        return RunResult(
            scenario_name=contract.scenario,
            expected_status=expected_status_code,
            actual_status=response.status_code,
            correlation_id=correlation_header,
            verification=None,
            error_code="VERIFICATION_FAILED",
            status="FAIL",
        )

    return run_result
