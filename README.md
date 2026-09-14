# SignalContract

SignalContract checks security-event logs against a predefined contract. A contract
describes the field values an event must contain, such as who attempted an action,
what they targeted, and whether the action was denied.

The tool reads local files, validates their structure, and compares security events
against the contract.

SignalContract is currently a learning and thesis-development project.

## Current development setup

Python 3.12 or newer is required.

SignalContract uses [uv](https://docs.astral.sh/uv/) for dependency and environment
management.

### 1. Install uv

On Linux or macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify that uv is installed:

```bash
uv --version
```

### 2. Clone the repository

```bash
git clone https://github.com/grcic550/SignalContract.git
cd SignalContract
```

### 3. Install the project and dependencies

```bash
uv sync
```

This creates the project virtual environment and installs SignalContract together
with its dependencies.

There is no need to manually activate `.venv` when using `uv run`.

### 4. Verify the installation

```bash
uv run signalcontract --help
```

Run all examples below from the repository root so the fixture paths resolve.

## Commands

Validate a contract's structure and supported rules:

```bash
uv run signalcontract validate \
    --contract tests/fixtures/valid-contract.yaml
```

Compare an events file against a contract:

```bash
uv run signalcontract verify \
    --contract tests/fixtures/valid-contract.yaml \
    --events tests/fixtures/valid-events.json
```

Display usage information:

```bash
uv run signalcontract --help
uv run signalcontract verify --help
uv run signalcontract validate --help
```

Display the installed SignalContract version:

```bash
uv run signalcontract version
```

The contract's `version` field identifies the contract format independently of the
SignalContract application version.

## Input formats

### Contracts

Contracts are YAML mappings.

Only contract version `1` is currently supported, and the version must be an
integer.

A contract contains:

- `version`: the contract format version.
- `scenario`: a nonempty name describing the scenario.
- `expect`: a mapping of expected event fields to exact string values.

An empty `expect` mapping is structurally valid, but verification fails with
`NO_RULES_DEFINED`.

For example:

```yaml
version: 1
scenario: denied_admin_db_deletion

expect:
  event_type: authorization.denied
  actor: user-42
  action: delete_database
  target: prod_db
  outcome: denied
  reason: insufficient_privileges
```

Allowed expectation fields are:

- `event_type`
- `actor`
- `action`
- `target`
- `outcome`
- `reason`
- `timestamp`
- `correlation_id`

### Events

Events can be supplied in either of these formats:

- `.json`: an array of event objects.
- `.jsonl`: one event object per line. Blank lines are ignored.

Every event must contain nonempty values for:

- `event_type`
- `actor`
- `action`
- `target`
- `outcome`
- `reason`
- `timestamp`

`correlation_id` is optional.

For example:

```json
{
  "event_type": "authorization.denied",
  "actor": "user-42",
  "action": "delete_database",
  "target": "prod_db",
  "outcome": "denied",
  "reason": "insufficient_privileges",
  "timestamp": "2026-08-25T12:01:15Z"
}
```

For `.json` input, event objects must be placed inside an array:

```json
[
  {
    "event_type": "authorization.denied",
    "actor": "user-42",
    "action": "delete_database",
    "target": "prod_db",
    "outcome": "denied",
    "reason": "insufficient_privileges",
    "timestamp": "2026-08-25T12:01:15Z"
  }
]
```

For `.jsonl`, each event must be written as a complete JSON object on a single line.

## Matching behavior

Every expectation defined in the contract must match the same event.

SignalContract performs exact field comparisons.

If one or more events satisfy all expectations, verification passes and all matching
events are reported.

If verification fails, SignalContract provides a reason code describing why.

Current verification outcomes include:

- `SUCCESS`: one or more matching events were found.
- `NO_RULES_DEFINED`: the contract contains an empty `expect` mapping.
- `NO_MATCHING_EVENTS`: no relevant candidate event was found.
- `MISMATCHED_FIELDS`: relevant events exist, but one or more expected field values
  do not match.

When mismatched fields are found, SignalContract reports the expected and actual
values from the closest candidate event.

The tool does not currently:

- enforce time windows;
- automatically isolate events by correlation ID;
- validate timestamp formats;
- perform privacy checks.

A timestamp or correlation ID is compared only when it is explicitly included in
`expect`.

Input validation currently checks required event fields but does not enforce all
event-field types.

## Examples

### 1. Matching event

```bash
uv run signalcontract verify \
    --contract tests/fixtures/valid-contract.yaml \
    --events tests/fixtures/valid-events.json
```

Expected output without terminal colors:

```text
PASS: matched 1 event(s).

Match 1:
  Event Type: authorization.denied
  Actor: user-42
  Action: delete_database
  Target: prod_db
  Reason: insufficient_privileges
  Timestamp: 2026-08-25T12:01:15Z
  Outcome: denied
```

Exit code: `0`.

### 2. No matching event

```bash
uv run signalcontract verify \
    --contract tests/fixtures/valid-contract.yaml \
    --events tests/fixtures/unmatched-events.jsonl
```

Expected output:

```text
FAIL: NO_MATCHING_EVENTS
```

Exit code: `1`.

No relevant candidate event was found for comparison with the contract.

### 3. Mismatched fields

```bash
uv run signalcontract verify \
    --contract tests/fixtures/valid-contract.yaml \
    --events tests/fixtures/mismatched-events.json
```

Example output:

```text
FAIL: MISMATCHED_FIELDS
Mismatched Fields:
Field: outcome
Expected: denied
Actual: success
```

Exit code: `1`.

Relevant events were found, but the closest candidate did not satisfy every
expectation.

### 4. Contract with no rules

A contract containing:

```yaml
version: 1
scenario: no_rules_defined
expect: {}
```

is structurally valid, but verification fails:

```text
FAIL: NO_RULES_DEFINED
```

Exit code: `1`.

### 5. Malformed input

```bash
uv run signalcontract verify \
    --contract tests/fixtures/valid-contract.yaml \
    --events tests/fixtures/invalid-events.jsonl
```

The command reports the malformed JSONL line, for example:

```text
Error: Malformed JSONL line 2: ...
```

Exit code: `1`.

Malformed records are reported rather than silently skipped.

Verification failures and handled input errors both currently use exit code `1`.
Their messages and reason codes indicate the cause of the failure.

## Run the tests

Run the full test suite:

```bash
uv run pytest
```

For quieter output:

```bash
uv run pytest -q
```

Run the linter:

```bash
uv run ruff check .
```

Check formatting:

```bash
uv run ruff format --check .
```

Tests currently cover contract validation, event parsing, matching, verification,
and command-line behavior.

## Project status

SignalContract is under active development.

Planned areas of development include privacy-aware log validation, correlation-aware
verification, time-window rules, machine-readable verification output, and additional
security-event validation.