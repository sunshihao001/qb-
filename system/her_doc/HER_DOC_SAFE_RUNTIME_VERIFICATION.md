# HER_DOC Safe Runtime Verification

## Boundary

HER_DOC may inspect, map, queue, validate files, and run safe-mode validators. It may not perform live runtime side effects.

## Forbidden Actions

- real swap/sell/buy/bridge/transfer/mint/launch;
- wallet signing;
- private-key access;
- transaction broadcast;
- auto order;
- production deployment;
- scheduler activation for trading/runtime mutation;
- direct mutation of production policy without review.

## Allowed Safe Verification

- file existence checks;
- file read checks;
- YAML/JSON parse checks;
- schema conformance checks;
- static route inspection;
- Python import/compile checks;
- runner discovery;
- safe-mode `--dry-run`;
- `--paper-only` with inert sample or fixture;
- replay fixture execution with inert historical data;
- trace/audit file validation.

## Required Verification Packet

Every HER_DOC run should record:

```yaml
safe_mode: true
forbidden_actions_detected: []
commands_run: []
files_checked: []
side_effect_scope: string
decision: SAFE_VERIFIED | SAFE_WITH_GAPS | BLOCKED | BLOCKED_FOR_LIVE_RISK
```

If any forbidden action is requested or detected, status must become `BLOCKED` or `BLOCKED_FOR_LIVE_RISK`.
