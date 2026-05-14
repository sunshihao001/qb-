# 钱包结构分析系统全流程审计

- generated_at: `2026-05-08T01:48:00Z`
- overall_status: `PASS`

## Canonical Route

- modules/source_wallet_bot
- modules/wallet_data_guard
- sikk_candidate_wallet_structure_pipeline.py
- sikk_wallet_structure_gate.py
- sikk_same_source_grouping.py
- sikk_chip_control_state_machine.py
- sikk_candidate_state_machine.py / sikk_live_run.py

## Runtime Artifacts

- source_wallet_runner：present — `modules/source_wallet_bot/runner.py`
- source_wallet_gmgn_adapter：present — `modules/source_wallet_bot/gmgn_live_adapter.py`
- wallet_data_guard：present — `modules/wallet_data_guard/contamination_scan.py`
- candidate_wallet_pipeline：present — `sikk_candidate_wallet_structure_pipeline.py`
- wallet_structure_gate：present — `sikk_wallet_structure_gate.py`
- same_source_grouping：present — `sikk_same_source_grouping.py`
- chip_control_state_machine：present — `sikk_chip_control_state_machine.py`
- candidate_state_machine：present — `sikk_candidate_state_machine.py`
- pipeline_orchestrator：present — `run_sikk_gmgn_pipeline.py`

## 文档已有但运行接入不足

- none

## 已补全运行能力

- LONG_RUNNING_AUTO_RUNNER｜HIGH｜resolved：sikk_wallet_structure_auto_runner.py
- ACCEPTANCE_NOT_IN_PIPELINE_MANIFEST｜MEDIUM｜resolved：auto runner 每轮写 acceptance/system audit 引用。
- WALLET_GUARD_SYSTEM_WIDE_INDEX｜MEDIUM｜resolved：auto runner 聚合每轮 guard 状态。

## Safety Boundary

- paper_only: true
- read_only_collectors: true
- real_swap_enabled: false
- signing_enabled: false
- broadcast_enabled: false
