# 04 Task Plans

任务计划层负责把目标转换成可执行计划，并给每个任务绑定状态机。

## 基本原则

- 先计划，再执行。
- 先交接，再推进。
- 每个任务必须有状态。
- 没有状态，不允许进入执行循环。

## 任务状态机

```text
RECEIVED          已接收目标
SCOUTING          正在侦察
PLANNING          正在规划
READY_TO_EXECUTE  可以执行
EXECUTING         正在执行
VERIFYING         正在验证
RECOVERING        正在恢复
BLOCKED           被阻断
DONE              已完成
ARCHIVED          已归档
```

## 状态流转

```text
RECEIVED
↓
SCOUTING
↓
PLANNING
↓
READY_TO_EXECUTE
↓
EXECUTING
↓
VERIFYING
├── 验证通过 → DONE → ARCHIVED
├── 验证失败 → RECOVERING → PLANNING
└── 高风险 → BLOCKED
```

## 状态机要求

- 每次任务推进必须更新状态。
- 状态不能跳跃，除非有明确恢复记录。
- BLOCKED 必须说明阻断原因和解除条件。
- DONE 必须通过验证审计层。
- ARCHIVED 必须有报告和复盘记录。
