# SignalContract

SignalContract checks security-event logs against a predefined contract. A contract
describes the field values an event must contain, such as who attempted an action,
what they targeted, and whether the action was denied.

The tool reads local files, checks their structure, and compares events against
the contract. It is a learning and thesis project under development.

## Current development setup

Python 3.12 or newer is required. The commands below use the existing development
virtual environment, which has SignalContract and its dependencies installed.
From the repository root on Linux or macOS, activate it:

```bash
source .venv/bin/activate
signalcontract --help
```

Run all examples below from the repository root so the fixture paths resolve.

**Fresh-install limitation:** package building currently fails because
`src/signalcontract/__init__.py` is missing. The instructions above assume an
already configured development environment; they are not a fresh-clone setup
procedure. Packaging needs to be fixed before documenting that procedure.

## Commands

Validate a contract's structure and supported rules:

```bash
signalcontract validate --contract tests/fixtures/valid-contract.yaml
```

Compare an events file against a contract:

```bash
signalcontract verify --contract tests/fixtures/valid-contract.yaml --events tests/fixtures/valid-events.json
```

Display usage information:

```bash
signalcontract --help
signalcontract verify --help
signalcontract validate --help
```

The `version` command is also available. The contract's `version` field identifies
its format, independently of the application's release version.

## Input formats

Contracts are YAML mappings. Only contract version `1` is supported, and it must
be an integer. `scenario` identifies the scenario, and `expect` is a nonempty
mapping of field names to exact string values.

For example, [tests/fixtures/valid-contract.yaml](tests/fixtures/valid-contract.yaml)
expects a denied database-deletion event:

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

Allowed expectation names are `event_type`, `actor`, `action`, `target`, `outcome`,
`reason`, `timestamp`, and `correlation_id`.

Events can be supplied in either format:

- **`.json`:** an array of event objects.
- **`.jsonl`:** one event object per line. Blank lines are ignored.

Every event must contain nonempty `event_type`, `actor`, `action`, `target`,
`outcome`, `reason`, and `timestamp` fields. `correlation_id` is optional. Use string
values for these fields. For example:

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

For `.json` input, wrap event objects in an array. For `.jsonl`, write each object
on a single line. The examples below use files already included in the repository.

## Matching behavior

- Every expectation must match the **same event**.
- Events that do not satisfy the expectations are excluded from the matches.
- Zero matches means verification fails.
- One or more matches means verification passes; all matching events are reported.
- Supplied events are assumed to belong to one scenario run.

The tool performs exact comparisons. It does not currently enforce time windows
or automatically isolate events by correlation ID. A timestamp or correlation ID
is compared only when included in `expect`. Timestamp format validation, privacy
checks, and explanations of individual field mismatches are not yet implemented.
Input validation currently checks required event fields but does not enforce all
event-field types.

## Examples

### 1. Matching event

```bash
signalcontract verify --contract tests/fixtures/valid-contract.yaml --events tests/fixtures/valid-events.json
```

Expected output, without terminal colors:

```text
PASS: matched 1 event(s).

Match 1:
  Event Type:  authorization.denied
  Actor:  user-42
  Action:  delete_database
  Target:  prod_db
  Reason:  insufficient_privileges
  Timestamp:  2026-08-25T12:01:15Z
  Outcome:  denied
```

Exit code: `0`.

### 2. No matching event

```bash
signalcontract verify --contract tests/fixtures/valid-contract.yaml --events tests/fixtures/unmatched-events.jsonl
```

Expected error output:

```text
FAIL: No events matched the contract.
```

Exit code: `1`. The input is readable, but none of its events satisfies the contract.

### 3. Malformed input

```bash
signalcontract verify --contract tests/fixtures/valid-contract.yaml --events tests/fixtures/invalid-events.jsonl
```

Expected error output:

```text
Error: Malformed JSONL line 2: Expecting property name enclosed in double quotes: line 1 column 104 (char 103)
```

Exit code: `1`. The second line is incomplete JSON, so verification cannot finish.
The malformed record is reported rather than silently skipped.

Verification failures and handled input errors both currently use exit code `1`;
their messages explain the difference.

## Run the tests

With the development environment activated, run:

```bash
python -m pytest -q
```

Tests cover contract validation, event parsing, matching, and command-line behavior.
