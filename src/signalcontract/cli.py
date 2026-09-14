import typer
from signalcontract.contract import load_contract as parse_yaml
from signalcontract.events import parse_log_file
from signalcontract.matcher import matcher
from signalcontract.results import VerificationResult
from signalcontract.errors import SignalContractError

app = typer.Typer()

@app.command()
def verify(contract: str = typer.Option(..., "--contract"), 
           events: str = typer.Option(..., "--events")):

    """Verify events against the contract."""
    if not contract and not events:
        typer.secho("Error: No contract or events file provided.", fg=typer.colors.RED, bold=True, err=True)
        raise typer.Exit(code = 1)

    if not events:
        typer.secho("Error: No events file provided.", fg=typer.colors.RED, bold=True, err=True)
        raise typer.Exit(code = 1)

    if not contract:
        typer.secho("Error: No contract file provided.", fg=typer.colors.RED, bold=True, err=True)
        raise typer.Exit(code = 1)

    
    try:
        contract_data = parse_yaml(contract)
        event_models = parse_log_file(events)
        result = VerificationResult.from_matcher(contract_data, event_models)

    except SignalContractError as e:
        typer.secho(f"Error: {e}",fg=typer.colors.RED, bold=True, err=True)
        raise typer.Exit(code = 1)
    except FileNotFoundError as e:
        typer.secho(f"Error: File not found: {e.filename}",fg=typer.colors.RED, bold=True, err=True)
        raise typer.Exit(code = 1)


    if result.status == "PASS":
        typer.secho(f"PASS: matched {len(result.matched_events)} event(s).",fg=typer.colors.GREEN, bold=True)

        for index, event in enumerate(result.matched_events, start=1):
            typer.secho(
                f"\nMatch {index}:",
                fg=typer.colors.CYAN,
                bold = True
            )

            typer.echo(f"  Event Type:  {event.event_type}")
            typer.echo(f"  Actor:  {event.actor}")
            typer.echo(f"  Action:  {event.action}")
            typer.echo(f"  Target:  {event.target}")
            typer.echo(f"  Reason:  {event.reason}")
            typer.echo(f"  Timestamp:  {event.timestamp}")

            if event.outcome == "denied":
                outcome = typer.style(
                    event.outcome,
                    fg=typer.colors.RED,
                    bold=True
                )
            else:
                outcome = typer.style(
                    event.outcome,
                    fg=typer.colors.GREEN,
                    bold=True
                )

            typer.echo(f"  Outcome:  {outcome}")

        raise typer.Exit(code = 0)

    if result.status == "FAIL":
        typer.secho(f"FAIL: {result.reason_code}",fg=typer.colors.RED, bold=True, err=True)
        if result.mismatched_fields:
            typer.echo("Mismatched Fields:")
            for field, values in result.mismatched_fields.items():
                typer.echo(f"  Field: {field}")
                typer.echo(f"    Expected: {values['expected']}")
                typer.echo(f"    Actual: {values['actual']}")
        raise typer.Exit(code = 1)
    

@app.command()
def version():
    typer.echo("SignalContract 0.1.0")


@app.command()
def validate(contract: str = typer.Option(..., "--contract")):
    """Validate a contract file for correctness."""

    try:
        parse_yaml(contract)
        typer.secho(f"Contract file {contract} is valid.", fg=typer.colors.GREEN, bold=True)

    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, bold=True, err=True)
        raise typer.Exit(code = 1)
    
if __name__ == "__main__":
    app()