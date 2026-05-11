---
artifact_type: task_passport
status: active
generated_at: 2026-05-08T01:13:16Z
task_type: wallet_intel_semantic_integration
route_decision: wallet_intel_semantic_integration
---
# 任务护照 — Wallet Data Guard 接入 Upstream Prep Runner

## original_goal
用户确认：继续把可运行 scanner 接入现有 upstream prep runner。

## real_intent
在既有 Source Wallet Bot 上游准备/GMGN adapter 输出阶段增加污染扫描与来源 manifest，使 raw/normalized/intelligence/handoff 在进入后续钱包结构分析前先被污染识别与隔离标记。

## canonical_route
```text
modules/source_wallet_bot/gmgn_live_adapter.py
→ modules/source_wallet_bot/runner.py
→ modules/wallet_data_guard/
→ sikk_candidate_wallet_structure_pipeline.py
→ sikk_wallet_structure_gate.py
```

## target_files
```text
modules/source_wallet_bot/gmgn_live_adapter.py
tests/test_source_wallet_gmgn_live_adapter.py
```

## allowed_actions
- 仅把 `modules/wallet_data_guard` 作为保护层接入 Source Wallet Bot adapter/prep 输出。
- 生成 `manifest/wallet_data_guard_source_manifest.json`。
- 生成 `verification/wallet_data_guard_contamination_scan.json`。
- 返回结果增加 `wallet_data_guard_status`、`wallet_data_guard_scan_report`、`wallet_data_guard_manifest`。
- 保持 read-only / paper-only，不触发交易。

## forbidden_actions
- 不创建新的钱包分析主系统。
- 不改变 GMGN collector 的只读边界。
- 不删除/移动旧数据。
- 不把污染扫描结果当交易信号。
- 不读取/输出 secret、API key、private key。

## verification_method
- 先补测试并确认失败。
- 实现后跑 source wallet adapter 测试与 wallet_data_guard 测试。
- 验证返回字段和实际文件存在。
- 写入验证报告。
