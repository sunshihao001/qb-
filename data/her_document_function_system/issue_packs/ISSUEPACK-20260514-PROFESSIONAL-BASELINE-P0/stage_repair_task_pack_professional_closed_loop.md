# 专业化阶段修复任务包 / Professional Stage Repair Pack

- source_doc_id: `DOC-20260514-PROFESSIONAL-REQ-001`
- status: `READY_WITH_GAPS_REPAIR_QUEUE_READY`
- boundary: `safe-mode / paper-only / no signing / no real trade`

## P0 Cross-system blockers
- `CROSS_REPAIR_07_RUNNERS_REGISTRY`: 建立 runner_registry / phase_runner_binding / runner_failure_policy / validation_runner_registry
  - target: `sikk_stable_trader_os/07_runners`
  - application: R00 运行前判断 P01-P10 哪个 runner 合法可执行；无绑定则阻断真实 runtime。
- `CROSS_REPAIR_RUNTIME_GOAL_CONTEXT`: 建立 runtime_goal_context.schema / goal_consumption_report.schema / goal_context_loader
  - target: `00_control + modules/her_runtime_bridge`
  - application: 每轮运行必须证明 operator_goal→phase_goal→runner→artifact→acceptance 被读取。
- `CROSS_REPAIR_PHASE_OUTPUT_INDEX_TRACE`: 建立阶段输出统一索引与 runner trace
  - target: `00_control/phase_output_index.json + 00_trace/runner_execution_trace.yaml`
  - application: dashboard/验收/复盘只读统一索引，不直读临时输出。
- `CROSS_REPAIR_HANDOFF_CONSUMPTION_ACCEPTANCE`: 建立 handoff_consumption_status 与 runtime_acceptance_runner
  - target: `09_handoff + 08_acceptance + modules/her_runtime_bridge`
  - application: 上游输出必须被下游读取消费后，才允许升级状态。
- `CROSS_REPAIR_R00_RUNTIME_BLOCKER_MATRIX`: 建立 R00 runtime blocker matrix / token_case_manifest / phase_execution_plan
  - target: `R00 runtime readiness`
  - application: 真实 token 不直接进 paper；必须先通过 P01-P07。
- `CROSS_REPAIR_P09_P10_UPGRADE_LOOP`: 建立 review_to_upgrade_policy / failure_attribution / shadow_regression_approval package
  - target: `P09/P10`
  - application: 复盘结果进入受控升级候选，不直接改 live rules。

## Phase tasks
- `P01` FACT_CONTROLLER: `data_fact_handoff_packet.json`
  - priority: `P0_BLOCKING`
  - required_data: GMGN/OKX facts, source/time/confidence/missing_reason/permission
- `P02` TOKEN_MARKET_DATA: `token_market_fact_packet.json`
  - priority: `P1_HIGH`
  - required_data: quote/security/liquidity/base market facts
- `P03` WALLET_ENTITY: `wallet_entity_structure_packet.json`
  - priority: `P0_BLOCKING`
  - required_data: roles/same-source/funding paths/token distribution edges
- `P04` CHIP_STRUCTURE: `chip_structure_evidence_packet.json`
  - priority: `P0_BLOCKING`
  - required_data: chip inventory/cost band/distribution progress/反证
- `P05` EVIDENCE_CONTROL: `evidence_counterevidence_packet.json`
  - priority: `P1_HIGH`
  - required_data: evidence and counterevidence with confidence + contradiction status
- `P06` SCENARIO_RECOGNITION: `scenario_recognition_packet.json`
  - priority: `P1_HIGH`
  - required_data: 场景识别/风险分支/不确定性
- `P07` STRATEGY_GATE: `strategy_gate_decision_packet.json`
  - priority: `P0_BLOCKING`
  - required_data: EXCLUDE/RECORD/RISK_MONITOR/WATCH/PAPER_READY/READY_FOR_CONFIRMATION
- `P08` PAPER_PERMISSION: `paper_permission_packet.json`
  - priority: `P0_BLOCKING`
  - required_data: paper-only permission/risk boundary/no live execution
- `P09` REVIEW_REPLAY: `review_replay_packet.json`
  - priority: `P1_HIGH`
  - required_data: paper result replay/failure attribution/no rule mutation
- `P10` CONTROLLED_UPGRADE: `upgrade_candidate_packet.json`
  - priority: `P1_HIGH`
  - required_data: candidate/shadow/regression/approval/rollback
