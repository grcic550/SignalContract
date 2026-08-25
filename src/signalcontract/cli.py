import typer
from signalcontract.contract import parse_yaml
from signalcontract.events import parse_log_file
from signalcontract.matcher import matcher
from signalcontract.errors import SignalContractError

app = typer.Typer()

@app.command()
def verify(contract: str = typer.Option(..., "--contract"), 
           events: str = typer.Option(..., "--events")):
    
    """Verify events against the contract."""
    
    try:
        contract_data = parse_yaml(contract)
        event_models = parse_log_file(events)
        matched_events = matcher(contract_data, event_models)

    except SignalContractError as e:
        typer.echo(f"Error: {e}",fg=typer.colors.RED, bold=True, err=True)
        raise typer.Exit(code = 1)

    if matched_events:
        typer.secho(f"PASS: matched {len(matched_events)} event(s).",fg=typer.colors.GREEN, bold=True)

        for index, event in enumerate(matched_events, start=1):
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

    typer.echo(f"FAIL: No events matched the contract.",fg=typer.colors.RED, bold=True, err=True)
    raise typer.Exit(code = 1)

@app.command()
def version():
    typer.echo("SignalContract 0.1.0")
    
if __name__ == "__main__":
    app()