# Hermes Harness V2.1 Real Task Regression Verification

## Verification Scope

V2.1 verifies the new replayable real-task fixture regression layer:

- `23_real_task_regression/task_fixtures/`
- `23_real_task_regression/expected_outcomes/`
- `23_real_task_regression/error_taxonomy/`
- `09_scripts/hermes_v21_real_task_regression_run.py`
- `06_verification/tests/test_real_task_regression_v21.py`

## Boundary

This verification can prove fixture regression behavior only.
It must not claim live task reliability improvement without accumulated live task samples.

## Expected Commands

```bash
cd /root/sikk-gmgn/hermes_harness
python3 -m pytest 06_verification/tests/test_real_task_regression_v21.py -q
python3 09_scripts/hermes_v21_real_task_regression_run.py --fixture-set core --json
```

## Current Status

Verified in this upgrade run:

```text
V2.1 unit: 4 passed in 0.10s
V2.1 fixture run: 5/5 passed, overall_passed=true
Joint regression: 20 passed in 0.58s
```

Latest fixture run:

```text
run_id=v21.regression.20260509.022420
run_dir=/root/sikk-gmgn/hermes_harness/23_real_task_regression/regression_runs/v21.regression.20260509.022420
reliability_claim=fixture_regression_passed_not_proven_in_live_tasks
```
