---
artifact_type: task_passport
status: active
generated_at: 2026-05-07T23:12:33Z
task_type: wallet_intel_semantic_integration
route_decision: wallet_intel_semantic_integration
---
# 任务护照 — Wallet Data Guard 子模块

## original_goal
用户要求：把系统数据防污染策略做成一个子模块，单独建立目录，分层实现并写入钱包分析项目。

## real_intent
在既有 canonical 钱包结构分析系统内新增独立防污染子模块，防止 raw/facts/evidence/inference/handoff/state/report/compat/legacy 数据互相污染；同时不能另建钱包分析主系统。

## canonical_route
```text
modules/source_wallet_bot
→ sikk_candidate_wallet_structure_pipeline.py
→ sikk_wallet_structure_gate.py
→ sikk_candidate_state_machine.py / sikk_live_run.py
```

## new_submodule_scope
```text
modules/wallet_data_guard/
```

定位：数据防污染与写入/读取/扫描保护层。它是 canonical 钱包分析项目的保护子模块，不是新的钱包分析系统。

## allowed_actions
- 新建 `modules/wallet_data_guard/` 独立子模块目录。
- 新建对应测试 `tests/test_wallet_data_guard.py`。
- 实现分层规则、写入门禁、source manifest、contamination scan。
- 以可选方式接入 `sikk_candidate_wallet_structure_pipeline.py`，不改变主分析语义。
- 只写代码、测试、验证记录；不迁移旧数据。

## forbidden_actions
- 不删除旧目录。
- 不移动旧数据。
- 不覆盖旧任务包。
- 不读取或输出 secret/API key/private key/token。
- 不触发真实交易、签名、broadcast。
- 不把 `modules/wallet_data_guard/` 做成新的钱包分析主系统。
- 不让 compat 路线写 canonical decision。

## verification_method
- 先写测试并看失败。
- 实现后测试通过。
- 验证子模块目录存在。
- 验证污染扫描能识别至少：推断写入 facts、handoff 写入 facts、compat 写 canonical、state 回写 wallet_data、fallback 缺 mapping_id。
- 验证写入门禁能拒绝跨层写入。

## expected_outputs
```text
modules/wallet_data_guard/__init__.py
modules/wallet_data_guard/contracts.py
modules/wallet_data_guard/write_gate.py
modules/wallet_data_guard/source_manifest.py
modules/wallet_data_guard/contamination_scan.py
modules/wallet_data_guard/README.md
tests/test_wallet_data_guard.py
hermes_harness/06_verification/wallet_data_guard_verification_20260507_231233.md
```
