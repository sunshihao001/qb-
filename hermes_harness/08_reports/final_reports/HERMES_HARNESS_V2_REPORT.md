# Hermes Harness V2.0 Report

## 版本定位

Hermes Harness V2.0 定位为：**混合式判断运行时系统**。

它吸收两类 Harness 思想：

- **Claude Code 式运行时纪律**：query loop、工具调度、恢复路径、上下文治理、运行时审批。
- **Codex 式显式控制面**：规则注册表、thread / rollout / state bridge、tool schema、exec policy、permission decision。
- **Hermes 自有判断治理层**：judgment governance、reliability calibration、anti-self-deception、benchmark regression。

核心认知更新：Hermes 不是让 AI 更自由地做事，而是让不稳定 AI 在受控制度中做事。

## 新增模块

- `17_control_registry/`：显式控制面注册层，规则包含 `rule_id/source/type/scope/precedence/content/status/superseded_by`。
- `18_thread_rollout_state/`：任务线程、rollout event、state bridge 档案层。
- `19_exec_policy/`：tool schema、exec policy、permission decision、tool ledger。
- `20_context_budget/`：上下文预算与 compact 语义重建契约。
- `21_judgment_benchmark/`：判断基准集与 regression 目录。
- `22_anti_self_deception/`：反自欺审计面。

## 新增可运行脚本

- `09_scripts/hermes_exec_policy_check.py`：执行策略检查器，输出 allow / ask / deny、R0-R5 风险等级、matched policy。
- `09_scripts/hermes_v2_thread_rollout_run.py`：V2.0 thread / rollout / state bridge dry-run runner。

## 新增测试

- `06_verification/tests/test_hybrid_harness_v2.py`

覆盖：

- V2 核心目录存在；
- control registry JSONL schema 与 12 条不变式；
- exec policy allow/deny；
- thread rollout runner 产出 thread_state、rollout_events、state_bridge；
- context budget、benchmark、anti-self-deception 资产；
- 验证报告与最终报告存在且不夸大结论。

## 关键不变式

1. 每条规则必须有 source/type/scope/precedence。
2. 每个任务必须有 thread_id。
3. 每一轮动作必须写入 rollout event。
4. 每个 tool_call 必须有 tool_result。
5. 工具执行前必须经过 schema + policy + permission。
6. 上下文装配前必须经过 input governance。
7. context 超预算时必须 compact，而不是继续堆。
8. compact 目标是恢复工作语义，不是摘要历史。
9. 执行者不得验证自己。
10. 验证报告本身必须接受 meta-verification。
11. 同类恢复失败超过阈值必须熔断。
12. 任何记忆被引用前必须检查是否 stale / superseded。

## 反自欺边界

本次 V2.0 已建立结构、策略、runner、测试与报告，但：

- **链路可运行不等于真实跨轮可靠性已经被证明**。
- dry-run 只能证明 thread/rollout/state bridge 与 policy checker 可运行。
- 判断质量提升必须通过 `21_judgment_benchmark/` 后续真实样本回归证明。

## 未完成事项

- 尚未把 V2.0 runner 接入 Telegram 或 Hindsight；本次任务明确不接入。
- 尚未触发真实任务多轮 regression；当前只有首批 benchmark case 资产。
- 尚未把所有历史 V1.x 规则自动迁入 control registry；当前注册的是 V2.0 核心不变式。

## 下一版本建议

V2.1 应做：

```text
真实任务输入
→ 自动 thread 创建
→ rollout event 自动补账
→ exec policy 强制前置
→ independent verification
→ meta-verification
→ benchmark regression
→ memory lifecycle review
```

并用真实任务样本证明判断质量是否改善，而不是继续只写文档。
