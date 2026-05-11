# Hermes Harness Runtime System V2.1

- current_version: `V2.1`
- canonical_root: `/root/sikk-gmgn/hermes_harness/`
- canonical_runtime_route: `hermes_runtime_hook_autonomous_problem_loop`
- canonical_launcher: `09_scripts/hermes_runtime_hook_launcher.py`
- slash_commands: `/HER_START <problem>`, `/HER_SYSTEM_DESIGN <problem>`
- current_boundary: `fixture_regression_passed_not_proven_in_live_tasks`
- index_status: `canonical`

## 1. 本体定位

HER / Hermes Harness 不是普通提示词库，也不是单个 Skill。

它是 Hermes 的外部认知运行时，用来把复杂任务强制进入：

```text
入口识别
→ 控制面读取
→ 任务护照
→ 问题理解
→ 证据收集
→ 假设生成
→ 根因定位
→ 方案执行
→ 工具账本
→ 独立验证
→ 判断治理
→ 可靠性校准
→ 失败恢复
→ 复盘写回
→ 完成审计
```

核心原则：

```text
模型不是系统中心；Harness 才是控制中心。
```

## 2. 当前版本路线

```text
V1.0  = skeleton / directory system
V1.1  = control closure
V1.2  = runtime judgment closure
V1.3  = APUR autonomous problem understanding and resolution
V1.4  = runtime hook binding
V1.5  = upstream /HER_START and /HER_SYSTEM_DESIGN integration
V1.6  = judgment governance layer
V1.7  = reliability calibration layer
V2.0  = hybrid judgment runtime
V2.1  = real-task fixture regression layer
```

## 3. 强制入口规则

### 3.1 强制进入 HER runtime 的入口

```text
/HER_START <problem>
/HER_SYSTEM_DESIGN <problem>
```

这两个命令已接入 Hermes Agent upstream command handling，并调用：

```text
/root/sikk-gmgn/hermes_harness/09_scripts/hermes_runtime_hook_launcher.py
```

### 3.2 普通聊天边界

普通聊天消息不等同于 runtime hook。

如果没有 slash trigger 或明确 runtime hook 调用，执行路径可能只是：

```text
persona + memory + skills + tools
```

而不一定强制生成：

```text
runtime_state.json
tool_ledger.jsonl
problem_passport.md
runtime_completion_audit.md
```

因此，凡是要求 HER 底层逻辑完整闭环、系统设计、自动化执行、深层扫描、补全本体、修复控制面，都应优先使用：

```text
/HER_START <problem>
```

或：

```text
/HER_SYSTEM_DESIGN <problem>
```

## 4. Canonical layer map

### 00_startup

- role: 启动顺序、任务模式判断、是否允许执行。
- key_file: `00_startup/HERMES_BOOT_SEQUENCE.md`

### 01_control_plane

- role: 控制面规则、权限、路由、验证、恢复、上下文、记忆、Wallet-Intel 兼容规则。
- key_files:
  - `01_control_plane/task_routing_policy.md`
  - `01_control_plane/runtime_hook_policy_v1_4.md`
  - `01_control_plane/judgment_governance_policy_v1_6.md`
  - `01_control_plane/reliability_calibration_policy_v1_7.md`

### 02_task_intake

- role: 任务接收、task passport、原始用户请求归档。

### 03_task_runtime

- role: active state、checkpoint、compact snapshot、runtime project inventory。

### 04_memory

- role: memory index、memory write queue、revalidation log。
- rule: 未验证经验先进 `memory_write_queue.jsonl`，不得直接视为 verified memory。

### 05_templates

- role: runtime state、task route、verification templates。

### 06_verification

- role: 独立验证、测试、verification reports。
- rule: executor 不得自证完成；completion claim 必须有验证证据。

### 07_recovery

- role: failed verification / blocked task / retry plan / recovery reports。

### 08_reports

- role: final reports、scan reports、audit reports、phase reports。

### 09_scripts

- role: runnable entrypoints and checkers。
- key_files:
  - `09_scripts/hermes_runtime_hook_launcher.py`
  - `09_scripts/hermes_runtime_hook_run.py`
  - `09_scripts/hermes_problem_loop_run.py`
  - `09_scripts/hermes_judgment_governance_run.py`
  - `09_scripts/hermes_reliability_calibration_run.py`
  - `09_scripts/hermes_v21_real_task_regression_run.py`

### 10_audit

- role: audit independence, stale-rule audit, surface completion audit, task audit。

### 11_workflows

- role: canonical workflow definitions。
- key_files:
  - `11_workflows/problem_understanding_closed_loop_resolution.workflow.md`
  - `11_workflows/hermes_runtime_hook_autonomous_problem_loop.workflow.md`
  - `11_workflows/judgment_governance.workflow.md`
  - `11_workflows/reliability_calibration.workflow.md`

### 12_problem_loop / 13_problem_loop_templates

- role: V1.3 APUR loop runtime artifacts and templates。

### 14_runtime_hooks

- role: V1.4 runtime hook runs, runtime state, tool ledger, completion audit。
- output contract:
  - `runtime_state.json`
  - `tool_ledger.jsonl`
  - `problem_passport.md`
  - `runtime_completion_audit.md`

### 15_judgment_governance

- role: V1.6 判断治理。判断是否继续、停止、降级、交接。

### 16_reliability_calibration

- role: V1.7 可靠性校准。记录 expected vs observed，不把 dry-run 当真实可靠性提升。

### 17_control_registry

- role: V2.0 显式规则注册表。
- canonical_file: `17_control_registry/control_registry.jsonl`
- compatibility_note: 历史语义可能叫 `rule_registry.jsonl`，但当前 canonical registry 是 `control_registry.jsonl`。

### 18_thread_rollout_state

- role: V2.0 thread_id、rollout event、state bridge、global event log。

### 19_exec_policy

- role: V2.0 tool schema、permission decision、exec policy、tool ledger。

### 20_context_budget

- role: V2.0 context budget and compact semantic rebuild。
- key_files:
  - `20_context_budget/context_budget_policy.md`
  - `20_context_budget/compact_rebuild_policy.md`

### 21_judgment_benchmark

- role: V2.0 benchmark skeleton。
- note: V2.1 已将可回放真实任务样本升级到 `23_real_task_regression/`。

### 22_anti_self_deception

- role: 假完成、dry-run 混淆、文档-only、plan-vs-execution、自评分审计。

### 23_real_task_regression

- role: V2.1 real-task fixture regression。
- key_dirs:
  - `23_real_task_regression/task_fixtures/`
  - `23_real_task_regression/expected_outcomes/`
  - `23_real_task_regression/error_taxonomy/`
  - `23_real_task_regression/regression_runs/`

## 5. 读取优先级

处理 HER 本体任务时，读取顺序：

```text
1. HERMES_RUNTIME_SYSTEM_INDEX.md
2. README.md
3. 00_startup/HERMES_BOOT_SEQUENCE.md
4. 01_control_plane/task_routing_policy.md
5. 01_control_plane/runtime_hook_policy_v1_4.md
6. 11_workflows/hermes_runtime_hook_autonomous_problem_loop.workflow.md
7. 17_control_registry/control_registry.jsonl
8. 19_exec_policy/tool_schema_registry.jsonl
9. 20_context_budget/context_budget_policy.md
10. 20_context_budget/compact_rebuild_policy.md
11. 23_real_task_regression/README.md
12. 06_verification/tests/*
```

## 6. 验证命令

### Runtime hook dry-run

```bash
cd /root/sikk-gmgn/hermes_harness && python3 09_scripts/hermes_runtime_hook_launcher.py --dry-run --origin cli --problem '验证 HER runtime hook' --json
```

### V2.1 fixture regression

```bash
cd /root/sikk-gmgn/hermes_harness && python3 09_scripts/hermes_v21_real_task_regression_run.py --fixture-set core --json
```

### 联合测试

```bash
cd /root/sikk-gmgn/hermes_harness && python3 -m pytest \
  06_verification/tests/test_real_task_regression_v21.py \
  06_verification/tests/test_hybrid_harness_v2.py \
  06_verification/tests/test_reliability_calibration.py \
  06_verification/tests/test_runtime_hook_launcher.py \
  06_verification/tests/test_judgment_governance.py -q
```

## 7. 完成判断

HER V2.1 本体连接完整的最低标准：

```text
HER_CORE_CONNECTED = true
HER_RUNTIME_HOOK_CONNECTED = true
HER_UPSTREAM_COMMAND_CONNECTED = true
HER_V2_DATA_PRESENT = true
HER_TESTS_PASS = true
HER_INDEX_LAYER_COMPLETE = true
HER_NEEDS_CORE_REBUILD = false
```

边界声明：

```text
V2.1 fixture regression passed ≠ live task reliability proven.
```
