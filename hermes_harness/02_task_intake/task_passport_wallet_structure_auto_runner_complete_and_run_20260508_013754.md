---
artifact_type: task_passport
status: active
generated_at: 2026-05-08T01:37:54Z
task_type: wallet_intel_semantic_integration
route_decision: wallet_intel_semantic_integration
---
# 任务护照 — Wallet Structure Auto Runner 补全并执行

## user_goal
用户要求：补全 acceptance、wallet_data_guard 趋势索引、resume 等剩余体系能力后，执行全自动流程。

## canonical_route
```text
modules/source_wallet_bot
→ modules/wallet_data_guard
→ run_sikk_gmgn_pipeline.py
→ sikk_candidate_wallet_structure_pipeline.py
→ sikk_wallet_structure_gate.py
→ sikk_wallet_structure_auto_runner.py
```

## allowed_changes
- 修改 `sikk_wallet_structure_auto_runner.py`。
- 修改/补充 `tests/test_sikk_wallet_structure_auto_runner.py`。
- 运行 paper-only/read-only 全自动流程。
- 写 governed output 和 HER verification。

## required_features
1. 每轮调用 Source Wallet acceptance validator。
2. 生成长期 `guard_index/wallet_data_guard_trend_index.json`。
3. 支持 `resume=True` / `--resume` 从 checkpoint 继续。
4. 执行全自动流程并验证 manifest/checkpoint/audit/guard index。

## forbidden
- 不执行真实 swap。
- 不签名。
- 不广播。
- 不读取/输出 secret/private key/API key。
- 不创建并行钱包结构主系统。
