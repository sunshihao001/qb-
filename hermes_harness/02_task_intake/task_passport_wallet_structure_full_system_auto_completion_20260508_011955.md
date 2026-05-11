---
artifact_type: task_passport
status: active
generated_at: 2026-05-08T01:19:55Z
task_type: wallet_intel_semantic_integration
route_decision: wallet_intel_semantic_integration
---
# 任务护照 — 钱包结构分析系统全流程补全与长时间自动任务

## original_goal
用户要求：把钱包结构分析系统全流程看一遍，找出只有文档、没有接入系统体系的位置，补可运行代码；使用 HER 底层逻辑做一套全自动长时间任务，并完善钱包数据分析结构系统体系。

## route_decision
```text
wallet_intel_semantic_integration
```

## canonical_system
```text
modules/source_wallet_bot
→ modules/wallet_data_guard
→ sikk_candidate_wallet_structure_pipeline.py
→ sikk_wallet_structure_gate.py
→ sikk_same_source_grouping.py
→ sikk_chip_control_state_machine.py
→ sikk_candidate_state_machine.py / sikk_live_run.py
```

## intent_decomposition
1. 审计当前钱包结构分析系统全链路。
2. 找出制度文档已存在但未接入运行体系的位置。
3. 优先补可运行代码，而不是再写纯文档。
4. 增加全自动长时间任务 runner，支持持续循环、checkpoint/resume、污染扫描、acceptance、审计报告。
5. 保持 paper-only / readonly / no swap / no signing / no broadcast。

## allowed_actions
- 新增专用 runner / auditor / tests。
- 接入现有 canonical 钱包结构系统。
- 只写入 governed 输出目录与 HER 验证目录。
- 使用 fake runner/sample mode 验证长时间任务逻辑。

## forbidden_actions
- 不创建第二套钱包结构分析主系统。
- 不把 `sikk_sol_full_auto_workflow.py` 升级成主入口。
- 不读取/保存/输出 secret、API key、private key。
- 不执行真实交易、签名、广播、swap。
- 不删除/移动旧数据。

## verification
- TDD：先写失败测试。
- pytest 专项 + 相关集成测试。
- 锚点验证。
- 写 HER verification artifact。
