# Hermes Harness Runtime System V2.1

- current_version: `V2.1`
- canonical_root: `/root/sikk-gmgn/hermes_harness/`
- canonical_index: `HERMES_RUNTIME_SYSTEM_INDEX.md`
- canonical_runtime_route: `hermes_runtime_hook_autonomous_problem_loop`
- canonical_launcher: `09_scripts/hermes_runtime_hook_launcher.py`
- slash_commands: `/HER_START <problem>`, `/HER_SYSTEM_DESIGN <problem>`
- status: `CONNECTED_INDEX_COMPLETED`

This directory is the canonical HER / Hermes Harness runtime system. It includes the historical V1.0–V1.7 layers plus the V2.0 hybrid judgment runtime and V2.1 real-task fixture regression layer.

For current navigation, read `HERMES_RUNTIME_SYSTEM_INDEX.md` first. The index defines the canonical layer map, trigger boundaries, current registry names, validation commands, and completion criteria.

## Current runtime chain

```text
/HER_START or /HER_SYSTEM_DESIGN
→ 09_scripts/hermes_runtime_hook_launcher.py
→ hermes_runtime_hook_autonomous_problem_loop
→ runtime_state / tool_ledger / verification / recovery / audit
→ V1.6 judgment governance
→ V1.7 reliability calibration
→ V2.0 registry + exec policy + context budget
→ V2.1 real-task fixture regression boundary
```

## Important boundary

普通聊天消息不等同于完整 HER runtime hook。需要强制进入 HER 底层闭环时，使用 `/HER_START <problem>` 或 `/HER_SYSTEM_DESIGN <problem>`。

V2.1 能声明 `fixture regression passed`，但不能声明真实线上任务长期可靠性已证明。

## Canonical root

`/root/sikk-gmgn/hermes_harness/`

## V1.4 Runtime Hook extension

V1.4 binds V1.3 APUR into the Hermes/HER runtime entry path. Complex execution requests route through `hermes_runtime_hook_autonomous_problem_loop` and must externalize runtime state, tool ledger, verification hook, recovery hook, learning writeback, and completion audit.

Core artifacts:
- `01_control_plane/runtime_hook_policy_v1_4.md`
- `11_workflows/hermes_runtime_hook_autonomous_problem_loop.workflow.md`
- `14_runtime_hooks/`
- `09_scripts/hermes_runtime_hook_run.py`
- `06_verification/verification_reports/HERMES_HARNESS_V1_4_RUNTIME_HOOK_VERIFICATION.md`
- `08_reports/final_reports/HERMES_HARNESS_V1_4_RUNTIME_HOOK_REPORT.md`

## V1.3 core artifacts

- `HERMES_HARNESS_V1_3_AUTONOMOUS_PROBLEM_CLOSED_LOOP.md`
- `01_control_plane/problem_understanding_closed_loop_policy_v1_3.md`
- `11_workflows/problem_understanding_closed_loop_resolution.workflow.md`
- `05_templates/problem_understanding_closed_loop_state_schema_v1_3.json`
- `06_verification/problem_understanding_closed_loop_verification_checklist_v1_3.md`
- `07_recovery/problem_understanding_closed_loop_recovery_rule_v1_3.md`

## V1.3 structure

```text
hermes_harness/
├── 00_startup/
├── 01_control_plane/
├── 02_task_intake/
├── 03_task_runtime/
├── 04_memory/
├── 05_templates/
├── 06_verification/
├── 07_recovery/
├── 08_reports/
├── 09_scripts/
├── 10_audit/
└── 11_workflows/
```

## Core principle

```text
V1.0 is the skeleton.
V1.1 is the control closure.
V1.2 is the runtime judgment closure.
V1.3 is the autonomous problem-understanding and closed-loop resolution runtime.
```

## V1.3 cognitive chain

```text
问题接收
→ 自动理解
→ 证据收集
→ 假设生成
→ 根因定位
→ 方案生成
→ 执行
→ 验证
→ 失败恢复
→ 复盘写回
→ 下一轮更可靠判断
```

## Legacy policy

Legacy V1.0 docs remain at `docs/harness/ai_harness_system/` and are not deleted.
V1.1 artifacts remain as historical evidence unless superseded by explicit V1.2/V1.3 runtime policy.
V1.2 artifacts remain as the runtime-judgment base layer; V1.3 supersedes V1.2 only for problem-understanding and closed-loop resolution behavior.

## V1.3 APUR Loop Runtime Artifacts

- `12_problem_loop/` — APUR dry-run/runtime externalized judgment artifacts.
- `13_problem_loop_templates/` — APUR templates for passport, understanding, evidence, hypotheses, root cause, solution, verification, failure attribution, learning writeback, and loop state.
- `01_control_plane/auto_problem_solving_policy.md` — APUR control policy: no direct solution jump, no unverified memory write, CLOSED only after verification and memory queue.
- `09_scripts/hermes_problem_loop_run.py` — safe dry-run runner for APUR sample loops.

## V1.4 usable entrypoint

Use `09_scripts/hermes_runtime_hook_launcher.py` as the stable CLI/Gateway/quick-command surface. It wraps `hermes_runtime_hook_run.py` and returns JSON metadata for `runtime_run_id`, `run_dir`, `route`, and verification status. See `09_scripts/HER_RUNTIME_HOOK_QUICK_COMMANDS.md`.


## V1.5 Upstream HER commands

- `/HER_START <problem>` and `/HER_SYSTEM_DESIGN <problem>` are integrated into Hermes Agent upstream CLI/Gateway command handling.
- Upstream files: `/usr/local/lib/hermes-agent/hermes_cli/commands.py`, `/usr/local/lib/hermes-agent/cli.py`, `/usr/local/lib/hermes-agent/gateway/run.py`.
- Test file: `/usr/local/lib/hermes-agent/tests/cli/test_her_runtime_commands.py`.
- Verification: `08_reports/final_reports/HERMES_HARNESS_V1_5_UPSTREAM_HER_COMMANDS_REPORT.md`.


## V1.6 Judgment Governance Layer

V1.6 upgrades Hermes from closed-loop execution to judgment quality governance. It adds `hermes_judgment_governance_layer` and a `judgment_governance_hook` inside the V1.4 runtime hook.

Core artifacts:
- `HERMES_HARNESS_V1_6_JUDGMENT_GOVERNANCE_LAYER.md`
- `01_control_plane/judgment_governance_policy_v1_6.md`
- `11_workflows/judgment_governance.workflow.md`
- `15_judgment_governance/`
- `09_scripts/hermes_judgment_governance_run.py`
- `06_verification/tests/test_judgment_governance.py`
- `06_verification/HERMES_HARNESS_V1_6_JUDGMENT_GOVERNANCE_VERIFICATION_REPORT.md`
- `08_reports/final_reports/HERMES_HARNESS_V1_6_JUDGMENT_GOVERNANCE_REPORT.md`

Run:
```bash
cd /root/sikk-gmgn/hermes_harness && python3 09_scripts/hermes_judgment_governance_run.py --dry-run --problem 'Hermes 把 dry-run 当成真实完成' --json
```

## V1.7 Reliability Calibration Layer

V1.7 upgrades Hermes from “本轮判断治理通过” to “跨轮可靠性可校准”。It adds `hermes_reliability_calibration_layer` and a `reliability_calibration_hook` after `judgment_governance_hook` in the runtime hook.

Core artifacts:
- `HERMES_HARNESS_V1_7_RELIABILITY_CALIBRATION_LAYER.md`
- `01_control_plane/reliability_calibration_policy_v1_7.md`
- `11_workflows/reliability_calibration.workflow.md`
- `16_reliability_calibration/`
- `16_reliability_calibration/templates/reliability_calibration_state_template.json`
- `09_scripts/hermes_reliability_calibration_run.py`
- `06_verification/tests/test_reliability_calibration.py`

Run:
```bash
cd /root/sikk-gmgn/hermes_harness && python3 09_scripts/hermes_reliability_calibration_run.py --dry-run --problem 'Hermes 需要验证下一轮是否更可靠' --expected '下一轮降低假闭环' --observed 'dry-run 仅证明链路可运行' --json
```

## V2.0 Hybrid Judgment Runtime

V2.0 upgrades Hermes from a single-agent workflow into a hybrid Harness:

```text
Claude Code 式运行时纪律
+
Codex 式显式控制面
+
Hermes 自有判断治理 / 闭环学习层
```

Core artifacts:
- `17_control_registry/` — explicit rule registry with source/type/scope/precedence/status.
- `18_thread_rollout_state/` — thread_id, rollout events, state bridge, event log.
- `19_exec_policy/` — tool schema, exec policy, permission decisions, tool ledger.
- `20_context_budget/` — context budget and compact semantic rebuild policy.
- `21_judgment_benchmark/` — benchmark cases for judgment regression.
- `22_anti_self_deception/` — fake completion / dry-run / document-only / self-scoring audits.
- `09_scripts/hermes_exec_policy_check.py`
- `09_scripts/hermes_v2_thread_rollout_run.py`
- `06_verification/tests/test_hybrid_harness_v2.py`
- `06_verification/verification_reports/HERMES_HARNESS_V2_VERIFICATION.md`
- `08_reports/final_reports/HERMES_HARNESS_V2_REPORT.md`

Run:
```bash
cd /root/sikk-gmgn/hermes_harness && python3 09_scripts/hermes_v2_thread_rollout_run.py --problem 'Hermes Harness V2.0 混合式判断运行时 dry-run 验证' --dry-run --json
```

Verify:
```bash
cd /root/sikk-gmgn/hermes_harness && python3 -m pytest 06_verification/tests/test_hybrid_harness_v2.py 06_verification/tests/test_reliability_calibration.py 06_verification/tests/test_runtime_hook_launcher.py 06_verification/tests/test_judgment_governance.py -q
```

Boundary: V2.0 proves the hybrid runtime chain is runnable and auditable; it does **not** claim real cross-run reliability improvement until benchmark/regression evidence exists.

## V2.1 Real Task Regression Layer

V2.1 upgrades V2.0 from benchmark skeleton to replayable real-task fixture regression. It introduces concrete fixture cases, expected outcomes, judgment error taxonomy, per-run artifacts, memory lifecycle review, and meta-verification.

Core artifacts:
- `23_real_task_regression/task_fixtures/` — real-task-like fixture samples.
- `23_real_task_regression/expected_outcomes/` — expected decisions/actions for each fixture.
- `23_real_task_regression/error_taxonomy/` — judgment error taxonomy: fake completion, evidence insufficiency, unsafe execution, stale memory contamination, plan/execution confusion.
- `23_real_task_regression/regression_runs/` — generated replay runs with summary, case results, error log, memory lifecycle review, and anti-self-deception audit.
- `09_scripts/hermes_v21_real_task_regression_run.py`
- `06_verification/tests/test_real_task_regression_v21.py`
- `06_verification/verification_reports/HERMES_HARNESS_V2_1_REAL_TASK_REGRESSION_VERIFICATION.md`
- `08_reports/final_reports/HERMES_HARNESS_V2_1_REAL_TASK_REGRESSION_REPORT.md`

Run:
```bash
cd /root/sikk-gmgn/hermes_harness && python3 09_scripts/hermes_v21_real_task_regression_run.py --fixture-set core --json
```

Verify:
```bash
cd /root/sikk-gmgn/hermes_harness && python3 -m pytest 06_verification/tests/test_real_task_regression_v21.py -q
```

Boundary: V2.1 can claim `fixture regression passed`; it does **not** claim live task reliability improvement. 不等于线上真实任务可靠性已经被长期证明。
