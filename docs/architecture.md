SignalContract/
  ├── pyproject.toml
  ├── README.md
  ├── examples/
  │   ├── denied-admin-delete.yaml
  │   ├── events-pass.jsonl
  │   ├── events-missing.jsonl
  │   └── events-wrong-value.jsonl
  ├── src/signalcontract/
  │   ├── __init__.py
  │   ├── cli.py          # command arguments, exit code, terminal output
  │   ├── contract.py     # YAML loading + Contract validation
  │   ├── models.py       # Contract, SecurityEvent, source location types
  │   ├── events.py       # JSONL reading + event parsing
  │   ├── matcher.py      # pure matching logic; no files, no printing
  │   ├── verify.py       # coordinates contract + events + matcher
  │   ├── results.py      # VerificationResult and diagnostic dataclasses
  │   ├── privacy.py      # forbidden strings/control characters (later)
  │   └── errors.py       # expected domain errors only
  ├── tests/
  │   ├── unit/
  │   │   ├── test_contract.py
  │   │   ├── test_events.py
  │   │   ├── test_matcher.py
  │   │   └── test_privacy.py
  │   ├── integration/
  │   │   └── test_cli.py
  │   └── fixtures/
  │       ├── valid-contract.yaml
  │       ├── invalid-contract.yaml
  │       └── valid-events.jsonl
  └── docs/
      ├── architecture.md
      └── decisions.md