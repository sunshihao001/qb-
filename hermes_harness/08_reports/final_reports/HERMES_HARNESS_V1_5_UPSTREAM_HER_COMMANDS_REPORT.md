# Hermes Harness V1.5 Upstream HER Runtime Commands Report

- generated_at: `2026-05-09T01:39:46Z`
- status: `PASSED`
- scope: Hermes Agent upstream CLI/Gateway minimal integration for `/HER_START` and `/HER_SYSTEM_DESIGN`
- canonical launcher: `/root/sikk-gmgn/hermes_harness/09_scripts/hermes_runtime_hook_launcher.py`
- route: `hermes_runtime_hook_autonomous_problem_loop`

## What changed

1. `hermes_cli/commands.py`
   - Registered `her-start` and `her-system-design` in `COMMAND_REGISTRY`.
   - Added underscore aliases `her_start` and `her_system_design`, enabling Telegram/Gateway-safe `/HER_START` and `/HER_SYSTEM_DESIGN` resolution.
   - Commands now appear in gateway help/known-command surfaces.

2. `cli.py`
   - Added HER launcher constant and default problem builder.
   - Added slash handling for canonical commands `her-start` and `her-system-design`.
   - CLI invokes launcher with `--origin cli --problem <payload> --json`.

3. `gateway/run.py`
   - Added HER launcher constant and default problem builder.
   - Gateway message intake invokes launcher with `--origin gateway --problem <payload> --json`.

4. `tests/cli/test_her_runtime_commands.py`
   - Added TDD coverage for command registry resolution, CLI launcher invocation, Gateway launcher invocation, and default problem fallback.

## Verification

### pytest_her_runtime_commands
- passed: `True`
- exit_code: `0`
- command: `python3 -m pytest tests/cli/test_her_runtime_commands.py -q`

```text
bringing up nodes...
bringing up nodes...

.....                                                                    [100%]
5 passed in 2.24s
```

### pytest_quick_and_gateway_regression
- passed: `True`
- exit_code: `0`
- command: `python3 -m pytest tests/cli/test_quick_commands.py tests/gateway/test_discord_slash_commands.py -q`

```text
bringing up nodes...
bringing up nodes...

.................................................                        [100%]
=============================== warnings summary ===============================
tests/gateway/test_discord_slash_commands.py::test_handle_thread_create_slash_reports_success
  /root/.local/share/uv/python/cpython-3.11.15-linux-x86_64-gnu/lib/python3.11/tokenize.py:427: RuntimeWarning: coroutine 'Process.communicate' was never awaited
    encoding, consumed = detect_encoding(readline)
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
49 passed, 1 warning in 2.86s
```

### compileall_targets
- passed: `True`
- exit_code: `0`
- command: `python3 -m compileall -q hermes_cli/commands.py cli.py gateway/run.py`

```text

```

### launcher_cli_dry_run
- passed: `True`
- exit_code: `0`
- command: `python3 09_scripts/hermes_runtime_hook_launcher.py --dry-run --origin cli --problem '执行任务，全自动完成：V1.5 upstream HER_START integration verification。' --json`

```text
{"status": "COMPLETED", "route": "hermes_runtime_hook_autonomous_problem_loop", "dry_run": true, "origin": "cli", "runtime_run_id": "runtime.20260509_013946.执行任务_全自动完成_V1_5_upstream_HER_STA", "run_dir": "/root/sikk-gmgn/hermes_harness/14_runtime_hooks/runtime_runs/runtime.20260509_013946.执行任务_全自动完成_V1_5_upstream_HER_STA", "overall_passed": true, "entrypoint": "/root/sikk-gmgn/hermes_harness/09_scripts/hermes_runtime_hook_launcher.py", "runner": "/root/sikk-gmgn/hermes_harness/09_scripts/hermes_runtime_hook_run.py", "contract": {"runtime_state": "runtime_state.json", "tool_ledger": "tool_ledger.jsonl", "problem_passport": "problem_passport.md", "completion_audit": "runtime_completion_audit.md"}}
```

## Completion audit

- result: `PASSED`
- recovery_report_required: `false`
- completion_condition: command registry + CLI handler + Gateway handler + launcher dry-run verified.
