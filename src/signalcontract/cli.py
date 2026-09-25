from importlib.metadata import version as package_version

import typer

from signalcontract.contract import load_contract as parse_yaml
from signalcontract.errors import SignalContractError
from signalcontract.events import parse_log_file
from signalcontract.runner import runner as run_test
from signalcontract.scenario import load_scenario
from signalcontract.verify import verify_contract

app = typer.Typer()


@app.command()
def verify(
    contract: str = typer.Option(..., "--contract"),
    events: str = typer.Option(..., "--events"),
    correlation_id: str | None = typer.Option(None, "--correlation-id"),
):
    """Verify events against the contract."""
    if not contract and not events:
        typer.secho(
            "Error: No contract or events file provided.",
            fg=typer.colors.RED,
            bold=True,
            err=True,
        )
        raise typer.Exit(code=1)

    if not events:
        typer.secho(
            "Error: No events file provided.", fg=typer.colors.RED, bold=True, err=True
        )
        raise typer.Exit(code=1)

    if not contract:
        typer.secho(
            "Error: No contract file provided.",
            fg=typer.colors.RED,
            bold=True,
            err=True,
        )
        raise typer.Exit(code=1)

    try:
        loaded_contract = parse_yaml(contract)

        if correlation_id is not None:
            if not correlation_id.strip():
                raise SignalContractError(
                    "correlation_id must be a non-empty string if provided."
                )
            loaded_contract.expect["correlation_id"] = correlation_id

        verify_result = verify_contract(loaded_contract, parse_log_file(events))

    except SignalContractError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, bold=True, err=True)
        raise typer.Exit(code=1) from None
    except FileNotFoundError as e:
        typer.secho(
            f"Error: File not found: {e.filename}",
            fg=typer.colors.RED,
            bold=True,
            err=True,
        )
        raise typer.Exit(code=1) from None

    if verify_result.status == "PASS":
        typer.secho(
            f"PASS: matched {len(verify_result.matched_events)} event(s).",
            fg=typer.colors.GREEN,
            bold=True,
        )

        for index, event in enumerate(verify_result.matched_events, start=1):
            typer.secho(f"\nMatch {index}:", fg=typer.colors.CYAN, bold=True)

            typer.echo(f"  Event Type: {event.event_type}")
            typer.echo(f"  Actor: {event.actor}")
            typer.echo(f"  Action: {event.action}")
            typer.echo(f"  Target: {event.target}")
            typer.echo(f"  Reason: {event.reason}")
            typer.echo(f"  Timestamp: {event.timestamp}")

            if event.outcome == "denied":
                outcome = typer.style(event.outcome, fg=typer.colors.RED, bold=True)
            else:
                outcome = typer.style(event.outcome, fg=typer.colors.GREEN, bold=True)

            typer.echo(f"  Outcome: {outcome}")

        raise typer.Exit(code=0)

    if verify_result.status == "FAIL":
        typer.secho(
            f"FAIL: {verify_result.reason_code}",
            fg=typer.colors.RED,
            bold=True,
            err=True,
        )

        if verify_result.mismatched_fields:
            typer.echo("Mismatched Fields:")

            for field, values in verify_result.mismatched_fields.items():
                typer.echo(f"Field: {field}")
                typer.echo(f"Expected: {values['expected']}")
                typer.echo(f"Actual: {values['actual']}")

        raise typer.Exit(code=1) from None


@app.command()
def version():
    typer.echo(f"SignalContract {package_version('signalcontract')}")


@app.command()
def validate(contract: str = typer.Option(..., "--contract")):
    """Validate a contract file for correctness."""

    try:
        parse_yaml(contract)

        typer.secho(
            f"Contract file {contract} is valid.", fg=typer.colors.GREEN, bold=True
        )

    except SignalContractError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, bold=True, err=True)

        raise typer.Exit(code=1) from None

    except FileNotFoundError as e:
        typer.secho(
            f"Error: File not found: {e.filename}",
            fg=typer.colors.RED,
            bold=True,
            err=True,
        )

        raise typer.Exit(code=1) from None


@app.command()
def run(
    url: str = typer.Option(..., "--url"),
    request_method: str = typer.Option(..., "--method"),
    request_path: str = typer.Option(..., "--path"),
    expected_status_code: int = typer.Option(..., "--expected-status"),
    contract_path: str = typer.Option(..., "--contract"),
    event_log_path: str = typer.Option(..., "--events"),
):
    """Run a test against a contract and return the result."""

    try:
        run_result = run_test(
            url,
            request_method,
            request_path,
            expected_status_code,
            contract_path,
            event_log_path,
        )

        if run_result.status == "PASS":
            typer.secho(
                f"PASS: {run_result.scenario_name} - "
                f"Expected status: {run_result.expected_status}, "
                f"Actual status: {run_result.actual_status}",
                fg=typer.colors.GREEN,
                bold=True,
            )
            raise typer.Exit(code=0)

        if run_result.status == "FAIL":
            typer.secho(
                f"FAIL: {run_result.scenario_name} - "
                f"Expected status: {run_result.expected_status}, "
                f"Actual status: {run_result.actual_status}, "
                f"Error code: {run_result.error_code}",
                fg=typer.colors.RED,
                bold=True,
                err=True,
            )
            raise typer.Exit(code=1)

        if run_result.status == "ERROR":
            typer.secho(
                f"ERROR: {run_result.scenario_name} - "
                f"Error code: {run_result.error_code}",
                fg=typer.colors.RED,
                bold=True,
                err=True,
            )
            raise typer.Exit(code=1)

    except SignalContractError as e:
        typer.secho(
            f"Error: {e}",
            fg=typer.colors.RED,
            bold=True,
            err=True,
        )


@app.command()
def run_scenario(
    scenario_file: str = typer.Option(..., "--scenario"),
    url: str = typer.Option(..., "--url"),
    events: str = typer.Option(..., "--events"),
):
    """Run a test scenario defined in a YAML file
    against a contract and return the result."""

    try:
        scenario = load_scenario(scenario_file)

        run_result = run_test(
            url,
            scenario.request_method,
            scenario.request_path,
            scenario.expected_status,
            scenario.contract_path,
            events,
        )

        if run_result.status == "PASS":
            typer.secho(
                f"PASS: {run_result.scenario_name} - "
                f"Expected status: {run_result.expected_status}, "
                f"Actual status: {run_result.actual_status}",
                fg=typer.colors.GREEN,
                bold=True,
            )
            raise typer.Exit(code=0)

        if run_result.status == "FAIL":
            typer.secho(
                f"FAIL: {run_result.scenario_name} - "
                f"Expected status: {run_result.expected_status}, "
                f"Actual status: {run_result.actual_status}, "
                f"Error code: {run_result.error_code}",
                fg=typer.colors.RED,
                bold=True,
                err=True,
            )
            raise typer.Exit(code=1)

        if run_result.status == "ERROR":
            typer.secho(
                f"ERROR: {run_result.scenario_name} - "
                f"Error code: {run_result.error_code}",
                fg=typer.colors.RED,
                bold=True,
                err=True,
            )
            raise typer.Exit(code=1)
    except SignalContractError as e:
        typer.secho(
            f"Error: {e}",
            fg=typer.colors.RED,
            bold=True,
            err=True,
        )
        raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
