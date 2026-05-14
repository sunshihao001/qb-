# HER DFAFS 自动化任务清单包执行顺序

- package_id: `HER_DFAFS_AUTOMATION_TASK_PACKAGE_20260514T024816Z`
- status: `READY_FOR_SAFE_MODE_EXECUTION`
- source_review: `HER-DFAFS-SYSTEM-SELF-REVIEW-20260514`
- boundary: local files only, additive updates, no production policy activation, no trading/private-key/sign/broadcast actions.

## 执行总原则

该包不是摘要，而是给后续 runner / agent 直接消费的任务清单包：

```text
self_review gaps
→ task_package.json
→ normalized next_actions
→ safe-mode implementation batch
→ verification
→ writeback_manifest
→ next_task_manifest
```

## 推荐顺序

1. `TASK-P0-001` 补 K00 controller file pack。
2. `TASK-P0-002` 统一 O00 run shape。
3. `TASK-P0-003` 升级 F00 六类资产抽取。
4. `TASK-P1-004` 加强 V00 schema/field/status/ref 验证。
5. `TASK-P1-005` 生成 A00 artifact manifest / phase matrix / evidence bundle。
6. `TASK-P1-007` 建立 status code mapping 和 forbidden transition。
7. `TASK-P1-006` 强制 runtime index / health snapshot 写回。
8. `TASK-P1-008` 建立 H00/U00/G00 safe-mode upgrade executor plan。

## 第一批只建议执行

- `TASK-P0-001`

原因：K00 是入口 contract。没有 K00 controller pack 时，后续 O00 run shape、F00 资产抽取、V00/A00 验收都缺统一输入契约。

## 验收红线

- `READY_WITH_GAPS != ACCEPTED`
- 不得宣称 `PRODUCTION_READY`
- 不得宣称 `POLICY_ACTIVE`
- 不得宣称 `RUNNER_BOUND`
- 不得删除 legacy runtime 数据
- 所有补全都必须有 evidence/ref/test 或明确标记 `READY_WITH_GAPS`
