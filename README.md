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

Every event must contain a nonblank string for:

- `event_type`
- `actor`
- `action`
- `target`
- `outcome`
- `reason`
- `timestamp`

`correlation_id` is optional. It may be absent or `null`; when supplied as a
string, it must contain at least one non-whitespace character.

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

### Private fields

SignalContract rejects an entire events file if it contains a field named
`password`, `passwd`, `api_key`, `access_token`, `refresh_token`, or `secret`.
The check ignores letter case and includes nested objects and lists. It runs
before events are converted into models, so extra fields are checked too.

The error points to the event index or JSONL line without printing the private
value. A matching event elsewhere in the file does not cancel the error.
This checks field names; it does not detect every possible secret hidden in text.

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
- validate timestamp formats.

A timestamp is compared only when it is included in `expect`.

To check one particular request, include `correlation_id` in `expect` or supply
`--correlation-id` when running `verify`. A nonempty CLI value takes precedence
over the ID in the contract for that invocation; the YAML file is not changed.
If you omit the option, the contract is used as written.

The ID is another exact-match condition. Without one, an older matching event can
satisfy the contract. All supplied events still undergo validation and private-field
checks, including events with other IDs.

An empty or whitespace-only CLI ID is rejected as an input error. IDs do not have
to be UUIDs; any nonblank string is accepted and compared exactly as supplied.

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

## Try the demo app

The small FastAPI app in `examples/demo_app` simulates an attempt to delete a
database. It uses a fixed fictional user, John (`user-42`), whose role is `user`.
It returns `403 Forbidden` and writes a denial event. There is no real database
or login system in this demo.

After `uv sync`, start the app from the repository root:

```bash
uv run fastapi dev
```

Leave that terminal running. Open `http://127.0.0.1:8000/docs`, expand
`DELETE /databases/prod_db`, and choose **Try it out**, then **Execute**.
You can also send the request from a second terminal:

```bash
curl -i -X DELETE http://127.0.0.1:8000/databases/prod_db
```

The response includes an `X-Correlation-ID` header. The app writes that same ID
into `examples/demo_app/event_denied.jsonl`, alongside the denial details and a
UTC timestamp. Each denied request gets a new ID and adds one line to the file.

Copy the response ID and use it in the following command, replacing
`PASTE_RESPONSE_ID_HERE`:

```bash
uv run signalcontract verify \
    --contract tests/fixtures/valid-contract.yaml \
    --events examples/demo_app/event_denied.jsonl \
    --correlation-id PASTE_RESPONSE_ID_HERE
```

You should see `PASS: matched 1 event(s).` The HTTP response is a denial, but the
verification passes because the application recorded the denial your contract
expects.

### Check what happens when logging breaks

Keep the existing log, then temporarily comment out the demo's file-writing block.
Send another DELETE request and verify using its new response ID. The application
still returns `403`, but SignalContract should report `FAIL: MISMATCHED_FIELDS`:
the older event has a different correlation ID. Restore the file-writing block
afterward.

You can also temporarily change the logged `outcome` to `success`, send a new
request, and verify its ID. Verification should fail because the event contradicts
the expected `denied` outcome. Restore `denied` when finished.

The generated log is local demo output. Use the ID from each response rather than
reusing an ID from an earlier run.

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

The current version checks event fields, rejects forbidden private fields, and
supports exact matching for individual request IDs. The demo connects those checks
to events generated by an HTTP request.

Next steps include adding time-window rules and providing machine-readable
verification output.
