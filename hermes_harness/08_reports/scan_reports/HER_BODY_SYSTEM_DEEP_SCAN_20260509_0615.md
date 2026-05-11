# HER 本体设计系统深层扫描报告

- scan_time: `2026-05-09 06:15 UTC`
- scan_scope: `/root/sikk-gmgn/hermes_harness/` + Hermes Agent upstream command hook
- trigger: 用户询问“之前底层逻辑运行体系有记得有这个，现在更新版本怎么没有了，是否没连接好，深层扫描 her 本体设计系统数据判断是否需要补全”
- conclusion_status: `CONNECTED_BUT_INDEX_PARTIAL`

## 1. 总结判断

HER 底层逻辑运行体系没有丢失，核心链路仍然存在，并且从 V1.3 / V1.4 / V1.5 / V1.6 / V1.7 / V2.0 / V2.1 的主要运行产物均可找到。

当前问题不是“本体设计没了”，而是：

1. 顶层 README 仍以 `Hermes Harness V1.3` 命名，虽然内容已经写到 V2.1，容易让新版本看起来像没有 HER 深层体系。
2. V2.0/V2.1 后新增的目录缺少部分 README / INDEX，导致人读或 Agent 自动索引时不够显性。
3. 一些新版目录里的关键文件命名与历史记忆中的预期不同，例如实际存在 `17_control_registry/control_registry.jsonl`，不是 `rule_registry.jsonl`。
4. `/HER_START` 和 `/HER_SYSTEM_DESIGN` upstream 连接存在，并能调用 runtime hook launcher；但这是 dry-run/control-run 入口，不等于所有普通消息自动强制进入 HER 深层 runtime。
5. runtime hook 自检通过，但本轮扫描发现“索引/入口显化层”需要补全，而不是“核心运行层断开”。

## 2. 已确认存在的核心链路

### 2.1 HER canonical root

```text
/root/sikk-gmgn/hermes_harness/
```

目录存在，且包含：

```text
00_startup
01_control_plane
02_task_intake
03_task_runtime
04_memory
05_templates
06_verification
07_recovery
08_reports
09_scripts
10_audit
11_workflows
12_problem_loop
13_problem_loop_templates
14_runtime_hooks
15_judgment_governance
16_reliability_calibration
17_control_registry
18_thread_rollout_state
19_exec_policy
20_context_budget
21_judgment_benchmark
22_anti_self_deception
23_real_task_regression
```

### 2.2 V1.4 Runtime Hook 入口

确认存在：

```text
09_scripts/hermes_runtime_hook_launcher.py
09_scripts/hermes_runtime_hook_run.py
14_runtime_hooks/runtime_templates/runtime_hook_state_template.json
01_control_plane/runtime_hook_policy_v1_4.md
11_workflows/hermes_runtime_hook_autonomous_problem_loop.workflow.md
```

### 2.3 V1.5 upstream Hermes Agent 命令连接

确认存在并已接入：

```text
/usr/local/lib/hermes-agent/hermes_cli/commands.py
/usr/local/lib/hermes-agent/cli.py
/usr/local/lib/hermes-agent/gateway/run.py
```

命令注册：

```text
her-start
her-system-design
```

对应 slash 语义：

```text
/HER_START <problem>
/HER_SYSTEM_DESIGN <problem>
```

两者都指向：

```text
/root/sikk-gmgn/hermes_harness/09_scripts/hermes_runtime_hook_launcher.py
```

### 2.4 V1.6 判断治理层

确认存在：

```text
15_judgment_governance/
01_control_plane/judgment_governance_policy_v1_6.md
11_workflows/judgment_governance.workflow.md
09_scripts/hermes_judgment_governance_run.py
06_verification/tests/test_judgment_governance.py
```

### 2.5 V1.7 可靠性校准层

确认存在：

```text
16_reliability_calibration/
01_control_plane/reliability_calibration_policy_v1_7.md
11_workflows/reliability_calibration.workflow.md
09_scripts/hermes_reliability_calibration_run.py
06_verification/tests/test_reliability_calibration.py
```

### 2.6 V2.0 Hybrid Judgment Runtime

确认存在：

```text
17_control_registry/control_registry.jsonl
17_control_registry/precedence_policy.md
17_control_registry/rule_scope_map.md
18_thread_rollout_state/state_bridge_index.md
19_exec_policy/tool_schema_registry.jsonl
20_context_budget/context_budget_policy.md
22_anti_self_deception/*.md
06_verification/tests/test_hybrid_harness_v2.py
```

注意：实际文件为：

```text
17_control_registry/control_registry.jsonl
```

不是历史记忆里可能出现的：

```text
17_control_registry/rule_registry.jsonl
```

### 2.7 V2.1 Real Task Regression

确认存在：

```text
23_real_task_regression/task_fixtures/rt_v21_001.json ... rt_v21_005.json
23_real_task_regression/expected_outcomes/
23_real_task_regression/error_taxonomy/
09_scripts/hermes_v21_real_task_regression_run.py
06_verification/tests/test_real_task_regression_v21.py
```

## 3. 本轮实测验证

### 3.1 联合测试结果

执行：

```bash
cd /root/sikk-gmgn/hermes_harness && python3 -m pytest \
  06_verification/tests/test_real_task_regression_v21.py \
  06_verification/tests/test_hybrid_harness_v2.py \
  06_verification/tests/test_reliability_calibration.py \
  06_verification/tests/test_runtime_hook_launcher.py \
  06_verification/tests/test_judgment_governance.py -q
```

结果：

```text
20 passed in 0.48s
```

### 3.2 Runtime Hook dry-run 结果

执行：

```bash
cd /root/sikk-gmgn/hermes_harness && python3 09_scripts/hermes_runtime_hook_launcher.py \
  --dry-run \
  --origin cli \
  --problem '深层扫描HER本体设计系统数据连接状态，判断是否需要补全' \
  --json
```

结果：

```json
{
  "status": "COMPLETED",
  "route": "hermes_runtime_hook_autonomous_problem_loop",
  "dry_run": true,
  "origin": "cli",
  "overall_passed": true
}
```

生成运行目录：

```text
/root/sikk-gmgn/hermes_harness/14_runtime_hooks/runtime_runs/runtime.20260509_061523.深层扫描HER本体设计系统数据连接状态_判断是否需要补全/
```

关键产物存在：

```text
runtime_state.json
tool_ledger.jsonl
problem_passport.md
runtime_completion_audit.md
```

`runtime_state.json` 显示 hook 均完成：

```text
router_hook: done
problem_passport_hook: done
judgment_governance_hook: done
apur_execution_hook: done
tool_ledger_hook: done
verification_hook: done
reliability_calibration_hook: done
learning_writeback_hook: done
completion_audit_hook: done
```

## 4. 发现的缺口

### GAP-01：顶层 README 标题与版本认知不一致

现状：

```text
# Hermes Harness V1.3
```

但 README 内容已经包含 V1.4 / V1.5 / V1.6 / V1.7 / V2.0 / V2.1。

影响：

- 人看会误以为当前还是 V1.3。
- Agent 自动读 README 时可能低估新版系统层。

建议：改成：

```text
# Hermes Harness Runtime System V2.1
```

并在顶部加 `current_version: V2.1` 与版本路线图。

### GAP-02：V2.0/V2.1 新目录缺少 README / INDEX

缺少或未找到：

```text
17_control_registry/README.md
18_thread_rollout_state/README.md
19_exec_policy/README.md
20_context_budget/README.md
21_judgment_benchmark/README.md
22_anti_self_deception/README.md
23_real_task_regression/README.md
```

影响：

- 深层扫描能找到文件，但普通入口不容易知道每层职责。
- 后续 HER 自己进行 context assembly 时，需要更明确的读取顺序。

### GAP-03：V2.0 文件命名与历史语义不完全一致

历史/记忆可能期待：

```text
17_control_registry/rule_registry.jsonl
```

实际存在：

```text
17_control_registry/control_registry.jsonl
```

这不是严重断链，但建议补一个索引说明或兼容别名，避免未来 Agent 查错文件。

### GAP-04：Context Budget 缺少独立 compact rebuild 文件

实际存在：

```text
20_context_budget/context_budget_policy.md
```

未找到：

```text
20_context_budget/compact_rebuild_policy.md
```

但 `context_budget_policy.md` 中已经写了 compact 语义。建议是否补独立文件取决于是否要把 compact 作为 V2.0 单独控制面。

### GAP-05：V2.1 benchmark 文件名不完全显性

未找到：

```text
21_judgment_benchmark/benchmark_cases.jsonl
```

但 V2.1 的实际 fixture 在：

```text
23_real_task_regression/task_fixtures/
23_real_task_regression/expected_outcomes/
```

建议补 `21_judgment_benchmark/README.md`，说明 V2.1 已将 benchmark skeleton 升级为 real-task fixture regression，主读取位置在 `23_real_task_regression/`。

### GAP-06：普通对话未必自动进入 HER runtime hook

`/HER_START` 和 `/HER_SYSTEM_DESIGN` 连接正常。

但如果用户直接普通发消息，不使用 slash command，也不触发 Hermes Agent 内部 gateway command handler，那么当前运行更多依赖模型读取 persona/memory/skills，而不是每条消息都由 runtime hook 强制接管。

这解释了为什么“更新版本看起来没有了”：

- 本体在 repo 里。
- slash command 接入在 upstream 里。
- 但当前普通聊天入口不一定每次都先执行 `/HER_START` runtime hook。

## 5. 是否需要补全

结论：需要补全，但不是补核心功能，而是补“索引显化层 + 兼容入口层”。

优先级：

### P0：不用补核心运行层

理由：核心文件、upstream 命令、runtime hook dry-run、V1.6/V1.7/V2.1 测试都通过。

### P1：建议补顶层版本索引

补：

```text
/root/sikk-gmgn/hermes_harness/HERMES_RUNTIME_SYSTEM_INDEX.md
/root/sikk-gmgn/hermes_harness/README.md
```

目标：让 Agent 一读就知道当前不是 V1.3，而是 V2.1 runtime system。

### P1：建议补 V2 层 README

补：

```text
17_control_registry/README.md
18_thread_rollout_state/README.md
19_exec_policy/README.md
20_context_budget/README.md
21_judgment_benchmark/README.md
22_anti_self_deception/README.md
23_real_task_regression/README.md
```

目标：让每个 runtime layer 都有职责、输入、输出、验收标准和读取顺序。

### P1：建议补兼容别名或索引

补：

```text
17_control_registry/rule_registry.jsonl
```

或更安全地补：

```text
17_control_registry/README.md
```

里面明确：

```text
canonical registry = control_registry.jsonl
legacy alias expectation = rule_registry.jsonl
```

不建议复制双份规则，避免两个 registry 漂移。

### P2：建议补 context compact 独立策略文件

补：

```text
20_context_budget/compact_rebuild_policy.md
```

目标：把“compact 是语义重建，不是历史摘要”从一行原则提升为可检查控制规则。

### P2：建议补当前入口说明

补：

```text
09_scripts/HER_RUNTIME_HOOK_QUICK_COMMANDS.md
```

已有，但可增加：

```text
普通聊天不等同于 runtime hook；强制进入 HER runtime 请使用 /HER_START 或 /HER_SYSTEM_DESIGN。
```

## 6. 推荐下一步执行包

如果要补全，建议按这个顺序：

1. 写 `HERMES_RUNTIME_SYSTEM_INDEX.md`。
2. Patch `README.md` 标题与 current_version。
3. 写 V2.0/V2.1 各目录 README。
4. 写 `20_context_budget/compact_rebuild_policy.md`。
5. Patch `09_scripts/HER_RUNTIME_HOOK_QUICK_COMMANDS.md` 加普通消息与 slash trigger 边界。
6. 跑联合测试：`20 passed`。
7. 跑 runtime hook dry-run。
8. 写补全审计报告。

## 7. 当前最终判断

```text
HER_CORE_CONNECTED = true
HER_RUNTIME_HOOK_CONNECTED = true
HER_UPSTREAM_COMMAND_CONNECTED = true
HER_V2_DATA_PRESENT = true
HER_TESTS_PASS = true
HER_INDEX_LAYER_COMPLETE = partial
HER_NEEDS_CORE_REBUILD = false
HER_NEEDS_INDEX_COMPLETION = true
```

一句话：

HER 本体设计系统没有断，底层逻辑还在；缺的是新版 V2.0/V2.1 的“总索引、目录说明、兼容命名说明、普通入口边界说明”，所以更新版本看起来像没连接好。建议补索引显化层，不建议重做核心运行层。
