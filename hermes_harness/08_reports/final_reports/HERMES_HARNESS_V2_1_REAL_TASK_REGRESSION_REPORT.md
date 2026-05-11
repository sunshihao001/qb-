# Hermes Harness V2.1 Real Task Regression Layer

## Version Position

V2.1 upgrades Hermes Harness from V2.0's hybrid judgment runtime skeleton into a replayable fixture-regression layer for real-task-like judgment cases.

```text
V2.0 Hybrid Judgment Runtime
→ V2.1 Real Task Regression Layer
```

## What V2.1 Adds

- Real-task fixture samples under `23_real_task_regression/task_fixtures/`
- Expected outcomes under `23_real_task_regression/expected_outcomes/`
- Judgment error taxonomy under `23_real_task_regression/error_taxonomy/`
- Regression runner: `09_scripts/hermes_v21_real_task_regression_run.py`
- Regression run artifacts: `23_real_task_regression/regression_runs/`
- Memory lifecycle review artifacts
- Meta-verification artifacts
- Anti-self-deception audit artifacts

## Core Judgment Boundary

V2.1 can say:

```text
fixture regression passed
```

V2.1 must not say:

```text
live task reliability has been proven
```

Chinese boundary:

```text
fixture regression passed 不等于线上真实任务可靠性已经被长期证明。
```

## Verification Entry

```bash
cd /root/sikk-gmgn/hermes_harness
python3 -m pytest 06_verification/tests/test_real_task_regression_v21.py -q
python3 09_scripts/hermes_v21_real_task_regression_run.py --fixture-set core --json
```

## Live Task Requirement

A live task reliability claim requires accumulated live task regression history, failure samples, recovery outcomes, and repeated regression reports. V2.1 is the bridge that makes those future measurements possible.
