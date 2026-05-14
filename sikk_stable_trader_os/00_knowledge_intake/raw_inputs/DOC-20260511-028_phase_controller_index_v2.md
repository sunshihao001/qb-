# `phase_controller_index.yaml`：P01-P10 业务阶段控制器总索引

这个文件的作用不是写业务逻辑，而是**注册每一个业务控制器的职责、输入、输出、追踪、验收、工具绑定权限、纸面运行权限和禁止事项**。

建议路径：

```text
/root/sikk-gmgn/system/phase_controllers/phase_controller_index.yaml
```

---

```yaml
schema_version: v2.0
file_id: PHASE_CONTROLLER_INDEX
file_name: phase_controller_index.yaml
system_name: SIKK Stable Trader OS
plane_level: light_institutional
status: DRAFT_READY_FOR_ACCEPTANCE

build_order_position:
  previous_stage: HANDOFF_PLANE
  current_stage: P01_P10_PHASE_CONTROLLERS
  next_stage:
    - RUNNER_TOOL_BINDING
    - PAPER_ONLY_RUNTIME
    - REVIEW_UPGRADE

purpose:
  primary: 注册 P01-P10 业务阶段控制器，定义每个控制器的职责、handoff 输入、输出合约、trace 要求、acceptance 要求、工具绑定权限、paper runtime 权限和禁止事项。
  secondary:
    - 防止业务控制器绕过 Full Control / Trace / Acceptance / Handoff
    - 防止业务控制器直接读取未交接文件
    - 防止业务控制器越权生成策略或执行结论
    - 为 Runner / Tool Binding 提供前置索引
    - 为 Paper-only Runtime 提供可运行阶段边界

global_rules:
  must_read_before_execution:
    - /root/sikk-gmgn/system/professional_build_order.md
    - /root/sikk-gmgn/system/full_control_plane/full_control_plane.yaml
    - /root/sikk-gmgn/system/trace_plane/trace_handoff_contract.yaml
    - /root/sikk-gmgn/system/acceptance_plane/acceptance_result_packet_contract.yaml
    - /root/sikk-gmgn/system/handoff_plane/handoff_packet_contract.yaml

  required_before_any_phase_controller:
    - trace_handoff_packet
    - acceptance_result_packet
    - handoff_packet
    - downstream_read_instruction
    - gap_propagation_packet
    - limitation_transfer_packet
    - field_usage_permission_packet

  forbidden_globally:
    - bypass_handoff_plane
    - bypass_acceptance_plane
    - bypass_trace_plane
    - read_unaccepted_artifacts
    - remove_gap_tags
    - remove_limitation_tags
    - convert_weak_use_to_full_use
    - generate_live_execution_signal
    - enable_auto_live_trade
    - mutate_governance_rules_without_review

phase_controllers:

  - phase_id: P01
    controller_id: P01_CANDIDATE_INTAKE_CONTROLLER
    controller_name_cn: 候选接收与基础对象建档控制器
    controller_type: BUSINESS_PHASE_CONTROLLER

    responsibility:
      primary: 接收候选代币，建立基础 token 对象、发现上下文、初始状态和候选档案。
      details:
        - 接收来自候选发现、人工输入、GMGN 热门榜、新币筛选或历史 replay 的 token 候选
        - 建立 token_address / pair_address / pool_address / discovery_time / discovery_market_cap_usd
        - 创建 candidate_id、candidate_status、initial_context
        - 不做钱包结构判断
        - 不做证据判断
        - 不做策略判断

    reads_handoff:
      required:
        - handoff_packet
        - downstream_read_instruction
        - governance_handoff_packet
        - domain_handoff_packet
        - data_requirement_handoff
      optional:
        - legacy_candidate_mapping_packet
        - manual_candidate_input_packet

    input_contracts:
      required:
        - candidate_intake_input_contract
        - token_identity_contract
        - discovery_context_contract
      optional:
        - manual_review_note_contract

    output_contracts:
      required:
        - candidate_registry_contract
        - token_identity_output_contract
        - candidate_intake_handoff_contract
      outputs:
        - candidate_registry.json
        - candidate_registry.csv
        - candidate_intake_summary.md
        - p01_candidate_intake_handoff_packet.yaml

    required_trace:
      - PHASE_TRACE
      - TASK_TRACE
      - ARTIFACT_TRACE
      - CONTRACT_TRACE
      - STATE_TRACE

    required_acceptance:
      gate_id: GATE_P01_CANDIDATE_INTAKE_READY
      accepted_status:
        - ACCEPTANCE_READY
        - ACCEPTANCE_READY_WITH_GAPS

    tool_binding:
      allowed: true
      mode:
        - READ_ONLY_DISCOVERY_TOOL
        - DRY_RUN_ONLY
      allowed_tools:
        - gmgn_candidate_discovery_readonly
        - manual_candidate_importer
      forbidden_tools:
        - trade_executor
        - wallet_signer
        - live_order_router

    paper_runtime:
      allowed: false
      reason: P01 只负责候选建档，不具备纸面运行权限。

    forbidden:
      - generate_evidence
      - classify_scenario
      - output_paper_ready
      - output_buy_signal
      - output_execution_permission
      - infer_dominant_side_intent
      - approve_runtime


  - phase_id: P02
    controller_id: P02_SOURCE_DATA_FACT_CONTROLLER
    controller_name_cn: 数据事实接收与标准化控制器
    controller_type: BUSINESS_PHASE_CONTROLLER

    responsibility:
      primary: 根据 P01 候选对象采集或接收事实数据，并转化为 raw / normalized / entity / event / snapshot 基础数据。
      details:
        - 读取候选 token 列表
        - 接收 GMGN、OKX、链上、K线、流动性、安全扫描等数据
        - 建立 raw 数据索引
        - 建立 normalized 数据结构
        - 建立数据质量、新鲜度、缺失和冲突记录
        - 不把数据直接转成证据
        - 不输出交易判断

    reads_handoff:
      required:
        - p01_candidate_intake_handoff_packet
        - data_plane_handoff_packet
        - field_usage_permission_packet
        - downstream_read_instruction
      optional:
        - legacy_data_mapping_packet

    input_contracts:
      required:
        - candidate_registry_contract
        - data_source_registry_contract
        - field_dictionary_contract
        - raw_data_contract
        - normalized_data_contract

    output_contracts:
      required:
        - source_data_fact_output_contract
        - normalized_fact_contract
        - data_quality_report_contract
        - p02_source_data_fact_handoff_contract
      outputs:
        - raw_data_index.json
        - normalized_token_facts.json
        - normalized_wallet_facts.json
        - normalized_market_facts.json
        - data_quality_report.json
        - data_missing_report.json
        - data_conflict_report.json
        - p02_source_data_fact_handoff_packet.yaml

    required_trace:
      - PHASE_TRACE
      - TASK_TRACE
      - ARTIFACT_TRACE
      - CONTRACT_TRACE
      - FIELD_TRACE
      - DATA_TRACE
      - STATE_TRACE

    required_acceptance:
      gate_id: GATE_P02_SOURCE_DATA_FACT_READY
      accepted_status:
        - ACCEPTANCE_READY
        - ACCEPTANCE_READY_WITH_GAPS

    tool_binding:
      allowed: true
      mode:
        - READ_ONLY_DATA_COLLECTION
        - DRY_RUN_ONLY
        - TEST_ONLY
      allowed_tools:
        - gmgn_token_data_reader
        - gmgn_wallet_data_reader
        - okx_quote_reader
        - okx_security_reader
        - kline_data_loader
        - data_normalizer
      forbidden_tools:
        - evidence_generator
        - strategy_gate_runner
        - trade_executor
        - wallet_signer

    paper_runtime:
      allowed: false
      reason: P02 只负责数据事实生产，不允许进入纸面运行。

    forbidden:
      - generate_evidence_strength
      - classify_wallet_intent
      - classify_trading_scenario
      - output_strategy_signal
      - output_paper_ready
      - approve_execution


  - phase_id: P03
    controller_id: P03_WALLET_ENTITY_CONTROLLER
    controller_name_cn: 钱包实体归并与角色初判控制器
    controller_type: BUSINESS_PHASE_CONTROLLER

    responsibility:
      primary: 对钱包地址进行实体归并、资金来源识别、同源候选识别、钱包基础角色初判。
      details:
        - 读取 P02 normalized_wallet_facts
        - 建立 wallet_entity
        - 建立 same_source_group_candidate
        - 建立 sync_buy_group_candidate
        - 建立 sync_sell_group_candidate
        - 输出钱包角色初判
        - 不直接推断主导侧意图
        - 不直接输出策略结论

    reads_handoff:
      required:
        - p02_source_data_fact_handoff_packet
        - domain_wallet_role_taxonomy_handoff
        - trace_handoff_packet
        - field_usage_permission_packet
      optional:
        - historical_address_library_handoff

    input_contracts:
      required:
        - normalized_wallet_fact_contract
        - wallet_entity_input_contract
        - wallet_role_taxonomy_contract
        - same_source_detection_contract

    output_contracts:
      required:
        - wallet_entity_output_contract
        - wallet_role_initial_classification_contract
        - wallet_group_candidate_contract
        - p03_wallet_entity_handoff_contract
      outputs:
        - wallet_entities.json
        - wallet_role_initial_classification.csv
        - same_source_group_candidates.json
        - sync_group_candidates.json
        - p03_wallet_entity_handoff_packet.yaml

    required_trace:
      - PHASE_TRACE
      - TASK_TRACE
      - ARTIFACT_TRACE
      - CONTRACT_TRACE
      - FIELD_TRACE
      - ENTITY_TRACE
      - STATE_TRACE

    required_acceptance:
      gate_id: GATE_P03_WALLET_ENTITY_READY
      accepted_status:
        - ACCEPTANCE_READY
        - ACCEPTANCE_READY_WITH_GAPS

    tool_binding:
      allowed: true
      mode:
        - READ_ONLY_ANALYSIS
        - TEST_ONLY
      allowed_tools:
        - wallet_entity_resolver
        - same_source_group_detector
        - wallet_role_classifier
      forbidden_tools:
        - strategy_gate_runner
        - trade_executor
        - live_wallet_manager

    paper_runtime:
      allowed: false
      reason: 钱包实体阶段只能产生结构事实和初判，不允许纸面交易。

    forbidden:
      - claim_market_maker_identity
      - output_dominant_side_intent_as_fact
      - output_buy_signal
      - output_paper_ready
      - approve_runtime
      - ignore_wallet_entity_uncertainty


  - phase_id: P04
    controller_id: P04_CHIP_STRUCTURE_CONTROLLER
    controller_name_cn: 筹码结构与迁移状态控制器
    controller_type: BUSINESS_PHASE_CONTROLLER

    responsibility:
      primary: 基于钱包实体、持仓变化、转账路径和市值上下文，判断筹码集中、留存、迁移、派发、对手盘压力等结构状态。
      details:
        - 计算 early_wallet_remaining_pct
        - 计算 structural_wallet_holding_pct
        - 计算 chip_concentration_score
        - 计算 chip_distribution_score
        - 识别 chip_transfer_status
        - 识别 counterparty_pressure_status
        - 生成筹码结构状态
        - 不直接生成策略准入

    reads_handoff:
      required:
        - p03_wallet_entity_handoff_packet
        - p02_source_data_fact_handoff_packet
        - domain_chip_structure_model_handoff
        - market_cap_context_handoff
        - field_usage_permission_packet
      optional:
        - historical_chip_pattern_handoff

    input_contracts:
      required:
        - wallet_entity_output_contract
        - wallet_group_candidate_contract
        - chip_structure_input_contract
        - market_cap_context_contract

    output_contracts:
      required:
        - chip_structure_output_contract
        - chip_migration_status_contract
        - counterparty_pressure_contract
        - p04_chip_structure_handoff_contract
      outputs:
        - chip_structure_summary.json
        - chip_migration_events.json
        - counterparty_pressure_summary.json
        - chip_structure_report.md
        - p04_chip_structure_handoff_packet.yaml

    required_trace:
      - PHASE_TRACE
      - TASK_TRACE
      - ARTIFACT_TRACE
      - CONTRACT_TRACE
      - FIELD_TRACE
      - ENTITY_TRACE
      - EVENT_TRACE
      - SNAPSHOT_TRACE
      - STATE_TRACE

    required_acceptance:
      gate_id: GATE_P04_CHIP_STRUCTURE_READY
      accepted_status:
        - ACCEPTANCE_READY
        - ACCEPTANCE_READY_WITH_GAPS

    tool_binding:
      allowed: true
      mode:
        - READ_ONLY_ANALYSIS
        - TEST_ONLY
      allowed_tools:
        - chip_structure_calculator
        - wallet_delta_snapshot_analyzer
        - counterparty_pressure_calculator
      forbidden_tools:
        - strategy_gate_runner
        - paper_trade_runner
        - live_trade_executor

    paper_runtime:
      allowed: false
      reason: P04 是结构分析阶段，不允许直接触发纸面交易。

    forbidden:
      - output_paper_ready
      - output_buy_signal
      - output_execution_permission
      - treat_partial_selling_as_auto_distribution_without_context
      - ignore_market_cap_context
      - ignore_trace_limitations


  - phase_id: P05
    controller_id: P05_EVIDENCE_CONTROLLER
    controller_name_cn: 证据与反证生成控制器
    controller_type: BUSINESS_PHASE_CONTROLLER

    responsibility:
      primary: 将可追踪、已交接的数据事实、钱包实体、筹码状态、市场结构转化为证据、反证、未知和冲突对象。
      details:
        - 读取 Trace / Handoff 允许使用的字段和事件
        - 生成 supporting_evidence
        - 生成 counter_evidence
        - 生成 uncertainty_tags
        - 标记 evidence_level
        - 标记 evidence_permission
        - 不直接识别完整交易场景
        - 不输出策略准入

    reads_handoff:
      required:
        - p04_chip_structure_handoff_packet
        - p03_wallet_entity_handoff_packet
        - p02_source_data_fact_handoff_packet
        - trace_handoff_packet
        - field_usage_permission_packet
        - limitation_transfer_packet
      optional:
        - review_evidence_feedback_handoff

    input_contracts:
      required:
        - evidence_input_contract
        - counter_evidence_input_contract
        - field_usage_permission_contract
        - uncertainty_tag_contract

    output_contracts:
      required:
        - evidence_object_contract
        - counter_evidence_object_contract
        - evidence_summary_contract
        - p05_evidence_handoff_contract
      outputs:
        - evidence_objects.json
        - counter_evidence_objects.json
        - evidence_summary.json
        - uncertainty_tags.json
        - p05_evidence_handoff_packet.yaml

    required_trace:
      - PHASE_TRACE
      - TASK_TRACE
      - ARTIFACT_TRACE
      - CONTRACT_TRACE
      - FIELD_TRACE
      - EVENT_TRACE
      - EVIDENCE_REF_TRACE
      - STATE_TRACE

    required_acceptance:
      gate_id: GATE_P05_EVIDENCE_CONTROLLER_READY
      accepted_status:
        - ACCEPTANCE_READY
        - ACCEPTANCE_READY_WITH_GAPS

    tool_binding:
      allowed: true
      mode:
        - READ_ONLY_ANALYSIS
        - TEST_ONLY
      allowed_tools:
        - evidence_builder
        - counter_evidence_builder
        - uncertainty_tagger
      forbidden_tools:
        - strategy_gate_runner
        - paper_trade_runner
        - trade_executor

    paper_runtime:
      allowed: false
      reason: 证据阶段只生成证据对象，不能进入纸面运行。

    forbidden:
      - classify_final_scenario_without_scenario_controller
      - output_strategy_gate_decision
      - output_paper_ready
      - upgrade_weak_evidence_to_strong_without_permission
      - ignore_counter_evidence
      - use_untraced_fields


  - phase_id: P06
    controller_id: P06_SCENARIO_RECOGNITION_CONTROLLER
    controller_name_cn: 多模型交易场景识别控制器
    controller_type: BUSINESS_PHASE_CONTROLLER

    responsibility:
      primary: 基于证据与反证识别当前代币处于何种交易场景，并输出场景候选、场景置信度、冲突场景和禁止误判。
      details:
        - 识别吸筹、控盘箱体、二段扩张、高位派发、下跌派发、诱多反抽、流动性陷阱等场景
        - 输出 primary_scenario_candidate
        - 输出 secondary_scenario_candidates
        - 输出 scenario_conflict
        - 输出 scenario_invalidations
        - 不直接输出交易准入
        - 不直接执行策略

    reads_handoff:
      required:
        - p05_evidence_handoff_packet
        - domain_scenario_taxonomy_handoff
        - trace_handoff_packet
        - acceptance_result_packet
        - limitation_transfer_packet
      optional:
        - historical_scenario_pattern_handoff

    input_contracts:
      required:
        - scenario_recognition_input_contract
        - evidence_summary_contract
        - counter_evidence_object_contract
        - scenario_taxonomy_contract

    output_contracts:
      required:
        - scenario_recognition_output_contract
        - scenario_conflict_contract
        - scenario_invalidation_contract
        - p06_scenario_handoff_contract
      outputs:
        - scenario_candidates.json
        - scenario_conflicts.json
        - scenario_invalidations.json
        - scenario_recognition_report.md
        - p06_scenario_handoff_packet.yaml

    required_trace:
      - PHASE_TRACE
      - TASK_TRACE
      - ARTIFACT_TRACE
      - CONTRACT_TRACE
      - EVIDENCE_REF_TRACE
      - DECISION_TRACE
      - STATE_TRACE

    required_acceptance:
      gate_id: GATE_P06_SCENARIO_RECOGNITION_READY
      accepted_status:
        - ACCEPTANCE_READY
        - ACCEPTANCE_READY_WITH_GAPS

    tool_binding:
      allowed: true
      mode:
        - READ_ONLY_ANALYSIS
        - TEST_ONLY
      allowed_tools:
        - scenario_classifier
        - scenario_conflict_detector
        - invalidation_checker
      forbidden_tools:
        - paper_trade_runner
        - live_trade_executor
        - wallet_signer

    paper_runtime:
      allowed: false
      reason: 场景识别不是策略门控，不允许直接进入纸面运行。

    forbidden:
      - output_paper_ready
      - output_buy_signal
      - output_execution_permission
      - ignore_counter_evidence
      - treat_scenario_candidate_as_strategy_approval
      - bypass_strategy_gate


  - phase_id: P07
    controller_id: P07_STRATEGY_GATE_CONTROLLER
    controller_name_cn: 策略准入与阻断控制器
    controller_type: BUSINESS_PHASE_CONTROLLER

    responsibility:
      primary: 基于场景、证据、反证、风险、限制标签和治理规则，判断候选是否进入 OBSERVE / PAUSE / BLOCK / PAPER_CANDIDATE / HUMAN_CONFIRMATION_REQUIRED。
      details:
        - 读取场景识别结果
        - 读取证据强度和反证
        - 读取治理硬否定规则
        - 读取 Handoff 限制标签
        - 判断是否允许进入 paper candidate
        - 明确阻断原因
        - 不执行交易
        - 不绕过 Execution Risk

    reads_handoff:
      required:
        - p06_scenario_handoff_packet
        - p05_evidence_handoff_packet
        - governance_handoff_packet
        - limitation_transfer_packet
        - forbidden_use_policy
        - field_usage_permission_packet
      optional:
        - strategy_pattern_profile_handoff

    input_contracts:
      required:
        - strategy_gate_input_contract
        - scenario_recognition_output_contract
        - evidence_summary_contract
        - governance_hard_negative_contract
        - limitation_transfer_contract

    output_contracts:
      required:
        - strategy_gate_decision_contract
        - strategy_block_reason_contract
        - p07_strategy_gate_handoff_contract
      outputs:
        - strategy_gate_decisions.json
        - strategy_gate_block_reasons.json
        - paper_candidate_candidates.json
        - strategy_gate_report.md
        - p07_strategy_gate_handoff_packet.yaml

    required_trace:
      - PHASE_TRACE
      - TASK_TRACE
      - ARTIFACT_TRACE
      - CONTRACT_TRACE
      - DECISION_TRACE
      - STATE_TRACE
      - ERROR_TRACE

    required_acceptance:
      gate_id: GATE_P07_STRATEGY_GATE_READY
      accepted_status:
        - ACCEPTANCE_READY
        - ACCEPTANCE_READY_WITH_GAPS

    tool_binding:
      allowed: true
      mode:
        - READ_ONLY_DECISION
        - TEST_ONLY
      allowed_tools:
        - strategy_gate_evaluator
        - hard_negative_rule_checker
        - limitation_enforcer
      forbidden_tools:
        - live_trade_executor
        - wallet_signer
        - auto_order_router

    paper_runtime:
      allowed: conditional
      condition:
        - strategy_gate_acceptance_ready
        - execution_risk_required
        - runtime_handoff_required
      reason: P07 可以产生 PAPER_CANDIDATE，但不能直接进入 Paper Runtime，必须经过 P08 Execution Risk 和 runtime_handoff。

    forbidden:
      - execute_trade
      - bypass_execution_risk
      - bypass_handoff_limitations
      - convert_observe_to_paper_ready_without_acceptance
      - ignore_governance_hard_negative
      - enable_live_execution


  - phase_id: P08
    controller_id: P08_EXECUTION_RISK_CONTROLLER
    controller_name_cn: 执行风控与纸面运行前门控控制器
    controller_type: BUSINESS_PHASE_CONTROLLER

    responsibility:
      primary: 对 P07 输出的 PAPER_CANDIDATE 进行报价、安全、滑点、流动性、仓位、风险限制和 paper-only 门控检查。
      details:
        - 检查 quote consistency
        - 检查 security risk
        - 检查 liquidity / slippage
        - 检查 daily loss limit
        - 检查 consecutive failure circuit breaker
        - 检查 one-token-one-live-position 约束
        - 输出 PAPER_RUNTIME_ALLOWED / BLOCKED / HUMAN_CONFIRMATION_REQUIRED
        - 保持 live execution forbidden

    reads_handoff:
      required:
        - p07_strategy_gate_handoff_packet
        - quote_security_handoff_packet
        - governance_execution_risk_rules
        - runtime_handoff_policy
        - limitation_transfer_packet
      optional:
        - paper_risk_history_handoff

    input_contracts:
      required:
        - execution_risk_input_contract
        - quote_security_contract
        - risk_control_contract
        - paper_runtime_precondition_contract

    output_contracts:
      required:
        - execution_risk_decision_contract
        - paper_runtime_permission_contract
        - p08_execution_risk_handoff_contract
      outputs:
        - execution_risk_decisions.json
        - quote_security_decisions.json
        - paper_runtime_permissions.json
        - execution_risk_report.md
        - p08_execution_risk_handoff_packet.yaml

    required_trace:
      - PHASE_TRACE
      - TASK_TRACE
      - ARTIFACT_TRACE
      - CONTRACT_TRACE
      - DECISION_TRACE
      - STATE_TRACE
      - ERROR_TRACE

    required_acceptance:
      gate_id: GATE_P08_EXECUTION_RISK_READY
      accepted_status:
        - ACCEPTANCE_READY
        - ACCEPTANCE_READY_WITH_GAPS

    tool_binding:
      allowed: true
      mode:
        - READ_ONLY_RISK_CHECK
        - TEST_ONLY
        - PAPER_ONLY_PRECHECK
      allowed_tools:
        - okx_quote_checker
        - okx_security_checker
        - slippage_estimator
        - paper_runtime_precheck
        - risk_event_logger
      forbidden_tools:
        - live_trade_executor
        - wallet_signer
        - auto_order_router

    paper_runtime:
      allowed: conditional
      condition:
        - execution_risk_acceptance_ready
        - runtime_handoff_exists
        - paper_only_flag_true
        - live_execution_forbidden
      reason: P08 可以允许进入 Paper-only Runtime，但不能允许自动实盘。

    forbidden:
      - approve_live_execution
      - bypass_paper_only_flag
      - ignore_security_risk
      - ignore_quote_deviation
      - ignore_slippage
      - run_without_runtime_trace


  - phase_id: P09
    controller_id: P09_REVIEW_REPLAY_CONTROLLER
    controller_name_cn: 复盘回放与失败归因控制器
    controller_type: BUSINESS_PHASE_CONTROLLER

    responsibility:
      primary: 对纸面运行、策略门控、场景识别、证据、数据、trace、handoff 结果进行复盘、回放和失败归因。
      details:
        - 读取 paper runtime 输出
        - 读取 runtime_trace
        - 重建当时输入状态
        - 区分数据问题、追踪问题、证据问题、场景问题、策略问题、执行风险问题
        - 输出 failure_attribution
        - 输出 review_case
        - 不直接修改实时规则
        - 不直接升级策略

    reads_handoff:
      required:
        - runtime_handoff_back_to_review
        - p08_execution_risk_handoff_packet
        - p07_strategy_gate_handoff_packet
        - trace_handoff_packet
        - paper_runtime_result_packet
      optional:
        - historical_review_case_library

    input_contracts:
      required:
        - review_replay_input_contract
        - runtime_trace_contract
        - paper_result_contract
        - failure_attribution_contract

    output_contracts:
      required:
        - review_case_contract
        - failure_attribution_output_contract
        - replay_result_contract
        - p09_review_replay_handoff_contract
      outputs:
        - review_cases.json
        - failure_attribution.jsonl
        - replay_results.json
        - review_replay_report.md
        - p09_review_replay_handoff_packet.yaml

    required_trace:
      - PHASE_TRACE
      - TASK_TRACE
      - ARTIFACT_TRACE
      - CONTRACT_TRACE
      - RUNTIME_TRACE
      - REVIEW_TRACE
      - STATE_TRACE

    required_acceptance:
      gate_id: GATE_P09_REVIEW_REPLAY_READY
      accepted_status:
        - ACCEPTANCE_READY
        - ACCEPTANCE_READY_WITH_GAPS

    tool_binding:
      allowed: true
      mode:
        - REPLAY_ONLY
        - REVIEW_ONLY
      allowed_tools:
        - replay_runner
        - failure_attribution_analyzer
        - paper_daily_report_reader
      forbidden_tools:
        - live_trade_executor
        - auto_strategy_mutator
        - governance_rule_writer_without_approval

    paper_runtime:
      allowed: false
      reason: P09 复盘已发生的纸面运行，不启动新的纸面交易。

    forbidden:
      - directly_mutate_strategy_rules
      - directly_update_governance_rules
      - treat_review_result_as_runtime_rule
      - ignore_runtime_trace
      - ignore_handoff_limitations


  - phase_id: P10
    controller_id: P10_SELF_UPGRADE_CONTROLLER
    controller_name_cn: 规则字段参数与系统升级控制器
    controller_type: BUSINESS_PHASE_CONTROLLER

    responsibility:
      primary: 根据 P09 复盘结果提出字段、规则、合约、验收门、trace、工具绑定、策略参数和方法论升级建议，并通过 Governance / Full Control / Acceptance 约束后进入系统更新。
      details:
        - 读取 review / replay 结果
        - 生成 upgrade_candidate
        - 判断升级类型
        - 输出 rollback_plan
        - 输出 governance_review_required
        - 不直接改实时系统
        - 不直接改执行规则
        - 不绕过 Acceptance

    reads_handoff:
      required:
        - p09_review_replay_handoff_packet
        - review_upgrade_handoff_packet
        - governance_review_policy
        - full_control_upgrade_routing_policy
      optional:
        - historical_upgrade_registry

    input_contracts:
      required:
        - self_upgrade_input_contract
        - review_case_contract
        - failure_attribution_output_contract
        - governance_review_contract
        - rollback_plan_contract

    output_contracts:
      required:
        - upgrade_candidate_contract
        - governance_review_request_contract
        - rollback_plan_output_contract
        - p10_self_upgrade_handoff_contract
      outputs:
        - upgrade_candidates.json
        - governance_review_requests.json
        - rollback_plans.json
        - self_upgrade_report.md
        - p10_self_upgrade_handoff_packet.yaml

    required_trace:
      - PHASE_TRACE
      - TASK_TRACE
      - ARTIFACT_TRACE
      - CONTRACT_TRACE
      - REVIEW_TRACE
      - UPGRADE_TRACE
      - STATE_TRACE

    required_acceptance:
      gate_id: GATE_P10_SELF_UPGRADE_READY
      accepted_status:
        - ACCEPTANCE_READY
        - ACCEPTANCE_READY_WITH_GAPS

    tool_binding:
      allowed: conditional
      mode:
        - PROPOSE_ONLY
        - DRY_RUN_ONLY
        - GOVERNANCE_APPROVED_UPDATE_ONLY
      allowed_tools:
        - upgrade_candidate_generator
        - config_diff_builder
        - schema_migration_planner
      forbidden_tools:
        - direct_runtime_rule_mutator
        - live_trade_executor
        - auto_deploy_without_acceptance

    paper_runtime:
      allowed: false
      reason: P10 只提出升级，不直接运行交易。

    forbidden:
      - directly_mutate_live_rules
      - bypass_governance_review
      - bypass_acceptance_rerun
      - deploy_without_rollback_plan
      - convert_review_suggestion_to_runtime_rule_without_approval
      - enable_live_execution

index_acceptance:
  required_gate: GATE_PHASE_CONTROLLER_INDEX_READY
  required_files:
    - phase_controller_index.yaml
  required_sections:
    - global_rules
    - phase_controllers
    - required_trace
    - required_acceptance
    - tool_binding
    - paper_runtime
    - forbidden
  pass_condition:
    - all_phase_controllers_registered
    - every_controller_has_responsibility
    - every_controller_has_handoff_inputs
    - every_controller_has_output_contracts
    - every_controller_has_trace_requirements
    - every_controller_has_acceptance_gate
    - every_controller_has_tool_binding_policy
    - every_controller_has_paper_runtime_policy
    - every_controller_has_forbidden_actions
    - live_execution_forbidden_globally

  fail_condition:
    - any_controller_missing_handoff
    - any_controller_missing_acceptance
    - any_controller_missing_trace
    - any_controller_can_bypass_handoff
    - any_controller_can_enable_live_execution
    - any_controller_outputs_beyond_authority
```

---

# 核心判断

这个 `phase_controller_index.yaml` 的作用是把 P01-P10 从“业务模块列表”升级成**受 Full Control / Trace / Acceptance / Handoff 管束的业务控制器体系**。

重点不是“每个阶段做什么”，而是每个阶段都必须回答：

```text
负责什么
读取什么 handoff
输出什么合约
需要什么 trace
需要什么 acceptance
能不能绑定工具
能不能进入 paper runtime
禁止什么
```

这套索引完成后，下一步才是逐个展开：

```text
P01 Candidate Intake Controller
P02 Source Data Fact Controller
P03 Wallet Entity Controller
P04 Chip Structure Controller
P05 Evidence Controller
P06 Scenario Recognition Controller
P07 Strategy Gate Controller
P08 Execution Risk Controller
P09 Review Replay Controller
P10 Self Upgrade Controller
```

---

# 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|每个 P01-P10 控制器的具体文件体系还未展开|目前只是总索引|下一步逐个展开 controller.yaml / context.md / contracts|
|每个控制器的 input/output contract 还未具体定义|已列名称|后续逐个补 schema|
|tool binding 只是权限定义|未绑定真实脚本|Runner / Tool Binding 阶段处理|
|paper runtime 只开放到 P08 后|还未运行|Paper-only Runtime 阶段处理|
|P05-P07 的业务规则还需后续细化|已定义边界|业务控制器展开时细化|
|P10 升级仍需 Governance 约束|已定义禁止绕过|后续 Governance review flow 补齐|