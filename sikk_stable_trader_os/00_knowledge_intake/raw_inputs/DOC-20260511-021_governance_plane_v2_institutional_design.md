# Governance Plane：治理平面专业机构化设计 v2.0

## 核心判断

`Governance Plane` 不能只是：

```text
系统禁止真实交易
系统要 paper-only
阶段要有权限
```

这种说明还不够专业。

专业级、轻量机构化水准的 `Governance Plane` 必须是：

```text
系统权限裁决层
  +
风险边界层
  +
硬否定规则层
  +
阶段权限矩阵
  +
真实交易禁用策略
  +
异常处理策略
  +
复盘升级边界
  +
违规检测与审计层
  +
Governance → Domain / Data / Control 的约束交接层
```

它的核心作用不是“写规则”，而是：

> **防止系统越权、误判、绕过阶段、跳过验收、错误进入 P01、错误进入 paper、错误进入真实交易。**

---

# 一、Governance Plane 在系统中的位置

当前完整链路应是：

```text
K00：知识摄取与 Phase Controller 候选任务化
  ↓
system_methodology_blueprint.md
  ↓
P00：系统建造与方法论编译控制器
  ↓
Bootstrap Control Plane：启动控制面
  ↓
Governance Plane：治理平面
  ↓
Domain Plane：领域平面
  ↓
Data Plane：数据平面
  ↓
Full Control Plane：完整控制面
  ↓
Trace / Acceptance / Handoff
  ↓
P01-P10 Phase Controller
  ↓
Runner / Paper-only Runtime / Review / Upgrade
```

`Governance Plane` 必须在 `Domain Plane` 和 `Data Plane` 之前建立。

原因：

```text
如果没有 Governance Plane，
Domain Plane 会不知道哪些判断允许定义，哪些判断必须使用证据语言；
Data Plane 会不知道哪些字段是阻断字段，哪些字段只能降级置信度；
P01-P10 会不知道自己的权限边界；
Runner 会不知道哪些操作禁止；
Review 会不知道复盘结果是否能直接修改实时规则。
```

---

# 二、Governance Plane 的最终定义

```text
Governance Plane 是 SIKK Stable Trader OS 的系统权限、风险边界、硬否定、阶段权限、真实交易禁用、异常处理和复盘升级控制平面。

它不负责分析 token。
它不负责判断钱包角色。
它不负责生成交易信号。
它不负责运行 paper trade。

它负责定义：

谁能做什么；
谁不能做什么；
什么情况必须阻断；
什么情况只能降级；
什么情况必须进入复盘；
什么情况禁止进入 P01；
什么情况禁止进入 paper；
什么情况永远禁止真实交易；
复盘结果如何进入 P10；
任何阶段如何被验收；
任何越权如何被记录和阻断。
```

一句话：

```text
Governance Plane 是系统的权限宪法和风险防火墙。
```

---

# 三、Governance Plane 必须解决的 12 个问题

```text
1. 每个阶段可以做什么，不能做什么？
2. 哪些阶段只有记录权，没有判断权？
3. 哪些阶段可以产生结构判断？
4. 哪些阶段可以裁决 paper permission？
5. 哪些阶段可以修改规则？
6. 哪些条件触发硬否定？
7. 哪些条件只能降级为 UNKNOWN？
8. 哪些条件必须阻断 P01？
9. 哪些条件必须阻断 paper runtime？
10. 哪些条件禁止真实交易？
11. 复盘结果如何进入系统升级？
12. 当不同阶段/文件发生冲突时，治理规则如何裁决？
```

---

# 四、专业机构级目录结构

建议固定为：

```text
/root/sikk-gmgn/sikk_stable_trader_os/00_governance/

  governance_plane.md
  authority_boundary.yaml
  stage_permission_matrix.yaml
  hard_negative_rules.yaml
  risk_boundary.yaml
  real_trade_forbidden_policy.yaml
  review_to_upgrade_policy.yaml
  evidence_language_policy.yaml
  assumption_control_policy.yaml
  exception_escalation_policy.yaml
  legacy_runtime_quarantine_policy.yaml
  runner_permission_policy.yaml
  governance_to_domain_constraints.yaml
  governance_to_data_constraints.yaml
  governance_to_control_constraints.yaml
  governance_readiness_gate.yaml
  governance_validation_rules.yaml
  governance_integrity_manifest.json
  governance_to_domain_handoff_packet.json
  governance_to_data_handoff_packet.json
  governance_event_log.jsonl

  schemas/
    authority_boundary.schema.json
    stage_permission_matrix.schema.json
    hard_negative_rules.schema.json
    risk_boundary.schema.json
    governance_handoff_packet.schema.json

  reports/
    governance_plane_acceptance_report.json
```

这套结构比只写一个 `governance_plane.md` 更专业，因为它同时覆盖：

```text
治理原则
阶段权限
风险边界
硬否定
真实交易禁用
证据语言
假设控制
异常升级
旧系统隔离
runner 权限
对 Domain / Data / Control 的下游约束
schema 校验
验收报告
完整性清单
事件日志
```

---

# 五、Governance Plane 核心文件设计

## 1. `governance_plane.md`

### 作用

治理平面总说明，供 HER / P00 / 后续阶段先读。

保存路径：

```text
00_governance/governance_plane.md
```

### 必须包含

````markdown
# Governance Plane：治理平面

## 1. 文件定位

Governance Plane 是 SIKK Stable Trader OS 的系统权限、风险边界、硬否定、阶段权限和真实交易禁用平面。

它不是策略文档。
它不是交易模型。
它不是钱包分析说明。
它是系统运行边界。

任何阶段在执行前，都必须受到 Governance Plane 约束。

---

## 2. 总原则

1. paper_only 永远为 true，除非未来有独立人工审批与真实交易安全系统。
2. real_trade_enabled 永远为 false。
3. P01 不得绕过 Data Plane。
4. P02-P10 不得绕过上游阶段。
5. Runner 不得绕过 Phase Controller。
6. 复盘结果不得直接修改实时规则，必须进入 P10。
7. 策略层不得读取未标准化原始数据直接裁决。
8. 执行层不得反向污染分析层。
9. 未知钱包不得强行分类。
10. 主导侧意图只能写成证据假设，不能写成确定事实。
11. 单一指标不得直接生成买点。
12. 缺少反证记录不得通过策略门禁。

---

## 3. 核心治理目标

Governance Plane 的目标是：

- 阻止非法阶段跃迁。
- 阻止未经数据验收的业务运行。
- 阻止真实交易。
- 阻止解释性语言污染证据判断。
- 阻止复盘结论直接污染实时规则。
- 阻止旧脚本未经注册进入正式系统。
- 阻止 runner 绕过 Phase Controller。
- 阻止 paper runner 绕过 P06 / P07。

---

## 4. 当前默认治理裁决

```json
{
  "paper_only": true,
  "real_trade_enabled": false,
  "p01_runtime_connection_allowed": false,
  "paper_runtime_allowed": false,
  "next_required_stage": "DOMAIN_AND_DATA_GOVERNED_GENERATION"
}
````

````

---

## 2. `authority_boundary.yaml`

### 作用

定义每个阶段的权限边界。

保存路径：

```text id="d9osfa"
00_governance/authority_boundary.yaml
````

### 标准内容

```yaml
authority_boundary_id: GOVERNANCE_AUTHORITY_BOUNDARY_001
version: 20260511_governance_plane_v2

global_authority_rules:
  - rule_id: GOV_AUTH_GLOBAL_001
    rule: no_stage_may_exceed_declared_authority_scope
    severity: P0
    action_on_violation: BLOCK_AND_LOG

  - rule_id: GOV_AUTH_GLOBAL_002
    rule: chat_context_is_not_authoritative_system_state
    severity: P0
    action_on_violation: REQUIRE_CURRENT_SYSTEM_STATE_READ

  - rule_id: GOV_AUTH_GLOBAL_003
    rule: real_trade_execution_is_forbidden
    severity: P0
    action_on_violation: HARD_BLOCK

stage_authority:
  K00_knowledge_intake_taskization:
    can:
      - save_input_assets
      - generate_document_passport
      - extract_methodology_requirements
      - generate_phase_controller_candidate_spec
      - generate_k00_to_p00_handoff_packet
    cannot:
      - register_formal_phase_controller
      - write_phase_registry
      - start_p01
      - generate_trade_signal
      - execute_real_trade
    decision_authority: candidate_only

  P00_system_bootstrap_controller:
    can:
      - consume_k00_handoff
      - consume_methodology_blueprint
      - create_bootstrap_control_plane
      - create_phase_registry
      - create_system_asset_index
      - block_p01
      - decide_next_legal_stage
    cannot:
      - run_p01
      - run_wallet_analysis
      - run_paper_trading
      - execute_real_trade
    decision_authority: system_bootstrap_authority

  P01_data_fact_controller:
    can:
      - read_data_plane_contracts
      - normalize_facts
      - generate_data_quality_report
      - output_normalized_fact
    cannot:
      - classify_wallet_roles
      - infer_dominant_side_intent
      - generate_trade_signal
      - allow_paper_trade
      - execute_real_trade
    decision_authority: fact_normalization_only

  P02_wallet_structure_controller:
    can:
      - classify_wallet_roles
      - detect_same_source_groups
      - generate_wallet_structure_report
    cannot:
      - approve_strategy_entry
      - execute_trade
      - modify_data_plane
    decision_authority: structural_inference_only

  P03_chip_control_controller:
    can:
      - infer_chip_control_status
      - calculate_counterparty_pressure
      - produce_dominant_side_status
    cannot:
      - approve_trade
      - run_paper_trade
      - modify_wallet_facts
    decision_authority: chip_control_inference_only

  P04_market_structure_controller:
    can:
      - evaluate_kline_volume_structure
      - evaluate_avwap_poc_structure
      - generate_market_structure_report
    cannot:
      - single_indicator_trade_signal
      - approve_paper_trade
      - override_wallet_risk
    decision_authority: market_structure_inference_only

  P05_scenario_classification_controller:
    can:
      - classify_scenario
      - record_supporting_evidence
      - record_contradicting_evidence
    cannot:
      - approve_paper_trade_without_P06
      - execute_trade
    decision_authority: scenario_classification_only

  P06_strategy_gate_controller:
    can:
      - approve_or_block_paper_candidate
      - generate_strategy_gate_decision
      - define_invalidation_conditions
    cannot:
      - execute_trade
      - bypass_execution_risk
      - enable_real_trade
    decision_authority: paper_permission_gate

  P07_execution_risk_controller:
    can:
      - simulate_execution_risk
      - evaluate_slippage_fee_liquidity
      - block_paper_execution_if_risk_unacceptable
    cannot:
      - override_P06_block
      - execute_real_trade
    decision_authority: paper_execution_risk_gate

  P08_paper_trading_controller:
    can:
      - run_paper_trade
      - record_paper_positions
      - record_paper_trades
    cannot:
      - enter_real_trade
      - alter_strategy_rules_directly
      - bypass_P06_P07
    decision_authority: paper_runtime_only

  P09_review_learning_controller:
    can:
      - attribute_failures
      - generate_rule_adjustment_candidates
      - generate_data_gap_feedback
    cannot:
      - directly_modify_realtime_rules
      - directly_modify_strategy_gate
    decision_authority: review_recommendation_only

  P10_system_upgrade_controller:
    can:
      - review_upgrade_candidates
      - propose_schema_migration
      - update_acceptance_rules_after_validation
    cannot:
      - enable_real_trade
      - bypass_backward_compatibility_check
    decision_authority: controlled_upgrade_authority
```

---

## 3. `stage_permission_matrix.yaml`

### 作用

定义阶段权限矩阵。

保存路径：

```text
00_governance/stage_permission_matrix.yaml
```

### 标准内容

```yaml
permission_matrix_id: STAGE_PERMISSION_MATRIX_001
version: 20260511_governance_plane_v2

permissions:
  - permission_id: READ_RAW_INPUT
    allowed_stages:
      - K00_knowledge_intake_taskization
    forbidden_stages:
      - P06_strategy_gate_controller
      - P08_paper_trading_controller

  - permission_id: WRITE_CONTROL_STATE
    allowed_stages:
      - P00_system_bootstrap_controller
      - FULL_CONTROL_PLANE
    forbidden_stages:
      - P01_data_fact_controller
      - P02_wallet_structure_controller
      - P08_paper_trading_controller

  - permission_id: NORMALIZE_FACTS
    allowed_stages:
      - P01_data_fact_controller
    forbidden_stages:
      - P02_wallet_structure_controller
      - P06_strategy_gate_controller
      - P08_paper_trading_controller

  - permission_id: CLASSIFY_WALLET_ROLE
    allowed_stages:
      - P02_wallet_structure_controller
    required_inputs:
      - normalized_wallet_fact
      - wallet_role_taxonomy
    forbidden_without:
      - P01_ACCEPTANCE_PASSED

  - permission_id: INFER_DOMINANT_SIDE_STATUS
    allowed_stages:
      - P03_chip_control_controller
    required_inputs:
      - wallet_classification
      - same_source_groups
      - chip_distribution_fact

  - permission_id: CLASSIFY_SCENARIO
    allowed_stages:
      - P05_scenario_classification_controller
    required_inputs:
      - wallet_structure_report
      - chip_control_status
      - market_structure_report

  - permission_id: APPROVE_PAPER_PERMISSION
    allowed_stages:
      - P06_strategy_gate_controller
    required_inputs:
      - scenario_classification
      - contradiction_report
      - risk_boundary
    forbidden_without:
      - P05_ACCEPTANCE_PASSED

  - permission_id: RUN_PAPER_TRADE
    allowed_stages:
      - P08_paper_trading_controller
    required_inputs:
      - paper_permission_packet
      - execution_risk_report
    forbidden_without:
      - P06_PAPER_ALLOWED
      - P07_EXECUTION_RISK_ACCEPTABLE

  - permission_id: MODIFY_RULES
    allowed_stages:
      - P10_system_upgrade_controller
    required_inputs:
      - failure_attribution_report
      - rule_adjustment_candidates
      - backward_compatibility_check
    forbidden_stages:
      - P08_paper_trading_controller
      - P09_review_learning_controller

  - permission_id: REAL_TRADE_EXECUTION
    allowed_stages: []
    forbidden_stages:
      - ALL
    hard_block: true
```

---

## 4. `hard_negative_rules.yaml`

### 作用

定义系统一票否决和强制阻断规则。

保存路径：

```text
00_governance/hard_negative_rules.yaml
```

### 标准内容

```yaml
hard_negative_rules_id: HARD_NEGATIVE_RULES_001
version: 20260511_governance_plane_v2

global_hard_negatives:
  - rule_id: HN_GLOBAL_001
    name_cn: 真实交易硬禁用
    condition: real_trade_enabled == true
    severity: P0
    action: FORCE_FALSE_AND_HARD_BLOCK
    applies_to:
      - ALL_STAGES

  - rule_id: HN_GLOBAL_002
    name_cn: 私钥或助记词出现
    condition: private_key_detected == true OR seed_phrase_detected == true
    severity: P0
    action: STOP_AND_QUARANTINE_INPUT
    applies_to:
      - ALL_STAGES

  - rule_id: HN_GLOBAL_003
    name_cn: P01 绕过 Data Plane
    condition: P01_requested == true AND data_plane_acceptance_passed != true
    severity: P0
    action: BLOCK_P01
    applies_to:
      - P01_data_fact_controller

  - rule_id: HN_GLOBAL_004
    name_cn: paper runner 绕过策略门禁
    condition: paper_runtime_requested == true AND P06_paper_permission != PAPER_ALLOWED
    severity: P0
    action: BLOCK_PAPER_RUNTIME
    applies_to:
      - P08_paper_trading_controller

  - rule_id: HN_GLOBAL_005
    name_cn: 执行层反向污染分析层
    condition: execution_result_attempts_to_modify_upstream_analysis == true
    severity: P0
    action: BLOCK_AND_ROUTE_TO_REVIEW
    applies_to:
      - P07_execution_risk_controller
      - P08_paper_trading_controller

  - rule_id: HN_GLOBAL_006
    name_cn: 复盘结果直接修改实时规则
    condition: review_output_directly_modifies_realtime_rule == true
    severity: P0
    action: BLOCK_AND_ROUTE_TO_P10
    applies_to:
      - P09_review_learning_controller

  - rule_id: HN_GLOBAL_007
    name_cn: 未知钱包强行分类
    condition: wallet_evidence_level == UNKNOWN AND wallet_role != UNKNOWN
    severity: P1
    action: DOWNGRADE_TO_UNKNOWN_AND_LOG
    applies_to:
      - P02_wallet_structure_controller

  - rule_id: HN_GLOBAL_008
    name_cn: 主导侧意图被写成确定事实
    condition: dominant_side_intent_language == DETERMINISTIC_FACT
    severity: P1
    action: REWRITE_AS_EVIDENCE_HYPOTHESIS
    applies_to:
      - P03_chip_control_controller
      - P05_scenario_classification_controller

  - rule_id: HN_GLOBAL_009
    name_cn: 单一指标直接给买点
    condition: trade_permission_generated_by_single_indicator == true
    severity: P0
    action: BLOCK_STRATEGY_GATE
    applies_to:
      - P04_market_structure_controller
      - P06_strategy_gate_controller

  - rule_id: HN_GLOBAL_010
    name_cn: 缺少反证记录却通过策略门禁
    condition: P06_decision == PAPER_ALLOWED AND contradiction_report_missing == true
    severity: P0
    action: BLOCK_PAPER_PERMISSION
    applies_to:
      - P06_strategy_gate_controller
```

---

## 5. `risk_boundary.yaml`

### 作用

定义系统风险边界。

保存路径：

```text
00_governance/risk_boundary.yaml
```

### 标准内容

```yaml
risk_boundary_id: RISK_BOUNDARY_001
version: 20260511_governance_plane_v2

risk_domains:
  system_risk:
    description: 系统状态、阶段流、文件一致性风险
    hard_blocks:
      - current_system_state_missing
      - phase_registry_missing
      - p01_ready_without_data_plane
      - conflicting_next_stage_unresolved

  data_risk:
    description: 数据字段、来源、质量、缺失风险
    hard_blocks:
      - required_field_missing_without_missing_policy
      - data_source_unknown
      - normalized_fact_schema_invalid
    downgrade_conditions:
      - optional_field_missing
      - stale_field_detected
      - low_quality_evidence

  wallet_structure_risk:
    description: 钱包角色、同源组、资金路径、筹码行为风险
    hard_blocks:
      - same_source_synchronized_exit_detected
      - active_distribution_detected
      - counterparty_pressure_extreme
      - core_wallet_structure_collapse
    downgrade_conditions:
      - insufficient_wallet_history
      - uncertain_funding_source
      - incomplete_current_holding_data

  market_structure_risk:
    description: K线、成交量、AVWAP、POC、疲劳风险
    hard_blocks:
      - fatigue_hard_negative_triggered
      - fake_breakout_with_volume_failure
      - control_box_breakdown_confirmed
      - avwap_loss_with_distribution
    downgrade_conditions:
      - weak_volume_confirmation
      - unclear_failure_test
      - insufficient_kline_window

  execution_risk:
    description: paper 执行模拟风险
    hard_blocks:
      - quote_security_failed
      - liquidity_too_low_for_paper
      - slippage_unbounded
      - fee_model_missing_for_execution
    downgrade_conditions:
      - quote_source_uncertain
      - fill_model_low_confidence

  governance_risk:
    description: 越权、跳阶段、真实交易、复盘污染风险
    hard_blocks:
      - real_trade_enabled_true
      - phase_bypass_detected
      - runner_bypass_detected
      - review_direct_rule_write_detected

default_actions:
  hard_block: BLOCK_AND_LOG
  downgrade: DOWNGRADE_CONFIDENCE_AND_REQUIRE_REVIEW
  unknown: SET_STATUS_UNKNOWN_AND_RECORD_GAP
```

---

## 6. `real_trade_forbidden_policy.yaml`

### 作用

真实交易禁用策略。

保存路径：

```text
00_governance/real_trade_forbidden_policy.yaml
```

### 标准内容

```yaml
policy_id: REAL_TRADE_FORBIDDEN_POLICY_001
version: 20260511_governance_plane_v2

default_real_trade_status: FORBIDDEN

global_flags:
  paper_only: true
  real_trade_enabled: false
  auto_order_allowed: false
  exchange_write_permission_allowed: false
  wallet_signing_allowed: false
  private_key_storage_allowed: false
  seed_phrase_storage_allowed: false

forbidden_actions:
  - create_real_order
  - submit_swap_transaction
  - sign_wallet_transaction
  - store_private_key
  - store_seed_phrase
  - enable_exchange_write_api
  - convert_paper_position_to_real_position
  - auto_execute_signal

allowed_actions:
  - paper_trade_simulation
  - quote_read_only
  - security_scan_read_only
  - execution_risk_simulation
  - human_review_note_generation

violation_response:
  on_real_trade_attempt:
    severity: P0
    action:
      - BLOCK
      - WRITE_GOVERNANCE_EVENT_LOG
      - WRITE_CURRENT_BLOCKERS
      - REQUIRE_MANUAL_REVIEW

  on_private_key_detected:
    severity: P0
    action:
      - STOP
      - QUARANTINE_INPUT
      - DO_NOT_STORE_SECRET
      - WRITE_SECURITY_EVENT
```

---

## 7. `review_to_upgrade_policy.yaml`

### 作用

定义复盘结果如何进入系统升级。

保存路径：

```text
00_governance/review_to_upgrade_policy.yaml
```

### 标准内容

```yaml
policy_id: REVIEW_TO_UPGRADE_POLICY_001
version: 20260511_governance_plane_v2

principle:
  review_outputs_are_not_realtime_rules: true
  p09_can_only_recommend: true
  p10_must_validate_before_upgrade: true

allowed_review_outputs:
  - failure_attribution_report
  - rule_adjustment_candidates
  - data_gap_feedback
  - scenario_misclassification_report
  - execution_model_error_report

forbidden_review_actions:
  - directly_modify_strategy_gate
  - directly_modify_data_schema
  - directly_modify_wallet_role_taxonomy
  - directly_modify_live_runtime_rules
  - directly_enable_real_trade

upgrade_path:
  - P09_review_learning_controller
  - P10_system_upgrade_controller
  - backward_compatibility_check
  - schema_migration_plan
  - acceptance_update_plan
  - control_plane_update
  - trace_matrix_update

p10_required_checks:
  - evidence_support_exists
  - sample_size_recorded
  - failure_pattern_repeated_or_high_severity
  - backward_compatibility_checked
  - rollback_plan_exists
  - acceptance_gate_updated
```

---

## 8. `evidence_language_policy.yaml`

### 作用

控制 AI 语言，防止把推断写成确定事实。

保存路径：

```text
00_governance/evidence_language_policy.yaml
```

### 标准内容

```yaml
policy_id: EVIDENCE_LANGUAGE_POLICY_001
version: 20260511_governance_plane_v2

allowed_language:
  - evidence_suggests
  - likely
  - possible
  - hypothesis
  - inferred_from
  - supported_by
  - contradicted_by
  - confidence_level

forbidden_language:
  - definitely_market_maker
  - must_pump
  - will_go_up
  - guaranteed
  - confirmed_intent_without_evidence
  -庄家一定
  -必拉
  -稳赚

dominant_side_language_rule:
  required_form: evidence_based_intent_hypothesis
  examples:
    allowed:
      - "当前证据支持主导侧仍可能保留部分筹码控制权。"
      - "该行为更符合洗盘/测试突破假设，但需要持仓 delta 进一步验证。"
    forbidden:
      - "庄家一定还没出货。"
      - "庄家一定要拉。"

confidence_required_for:
  - wallet_role_classification
  - same_source_group_detection
  - chip_control_status
  - dominant_side_lifecycle
  - scenario_classification
  - strategy_gate_decision
```

---

## 9. `assumption_control_policy.yaml`

### 作用

控制系统假设，避免 AI 用上下文幻想补字段。

保存路径：

```text
00_governance/assumption_control_policy.yaml
```

```yaml
policy_id: ASSUMPTION_CONTROL_POLICY_001
version: 20260511_governance_plane_v2

global_rules:
  - no_missing_field_may_be_filled_by_assumption
  - no_wallet_role_may_be_assigned_without_evidence
  - no_strategy_gate_may_pass_without_contradiction_review
  - no_data_source_may_be_invented
  - chat_context_cannot_replace_input_contract

assumption_labels:
  allowed:
    - ASSUMPTION
    - HYPOTHESIS
    - NEEDS_VERIFICATION
    - UNKNOWN
    - INSUFFICIENT_DATA

forbidden_assumptions:
  - assume_wallet_same_source_without_evidence
  - assume_current_holding_without_snapshot
  - assume_market_cap_without_source
  - assume_paper_entry_price_without_quote
  - assume_distribution_without_sell_flow
  - assume_accumulation_without_buy_flow

missing_data_policy:
  core_field_missing:
    action: BLOCK_OR_UNKNOWN
  optional_field_missing:
    action: DOWNGRADE_CONFIDENCE
  source_uncertain:
    action: REQUIRE_SOURCE_TRACE
```

---

## 10. `legacy_runtime_quarantine_policy.yaml`

### 作用

旧脚本、旧数据不能直接进入正式系统。

保存路径：

```text
00_governance/legacy_runtime_quarantine_policy.yaml
```

```yaml
policy_id: LEGACY_RUNTIME_QUARANTINE_POLICY_001
version: 20260511_governance_plane_v2

legacy_runtime_paths:
  - data/gmgn_candidates_live_run/
  - old_runtime_outputs/
  - legacy_scripts/

default_status: INDEX_ONLY_DO_NOT_DELETE_DO_NOT_DIRECTLY_CONSUME

allowed_actions:
  - index_legacy_asset
  - read_for_reference
  - map_to_new_contract
  - migrate_after_schema_validation
  - use_as_replay_sample_after_registration

forbidden_actions:
  - direct_use_as_current_runtime_state
  - direct_feed_into_p01_without_data_contract
  - direct_feed_into_strategy_gate
  - delete_without_backup
  - overwrite_new_system_state

migration_requirements:
  - asset_registered_in_system_asset_index
  - source_path_recorded
  - schema_mapping_defined
  - quality_check_passed
  - consumed_by_declared
  - trace_matrix_updated
```

---

## 11. `runner_permission_policy.yaml`

### 作用

定义 runner 权限边界。

保存路径：

```text
00_governance/runner_permission_policy.yaml
```

```yaml
policy_id: RUNNER_PERMISSION_POLICY_001
version: 20260511_governance_plane_v2

global_runner_rules:
  - runner_must_be_invoked_by_phase_controller
  - runner_must_have_input_contract
  - runner_must_have_output_contract
  - runner_must_write_validation_result
  - runner_must_not_bypass_acceptance_gate
  - runner_must_not_execute_real_trade

allowed_runner_types:
  - validation_runner
  - data_normalization_runner
  - wallet_structure_runner
  - market_structure_runner
  - paper_trade_runner
  - replay_runner
  - report_runner

forbidden_runner_actions:
  - direct_real_order_execution
  - wallet_signing
  - exchange_write_api_call
  - modifying_current_system_state_without_control_plane
  - writing_strategy_permission_without_P06

runner_failure_policy:
  on_input_missing: BLOCK_AND_REPORT
  on_schema_invalid: BLOCK_AND_REPORT
  on_runtime_error: WRITE_RISK_EVENT_AND_STOP
  on_output_missing: ACCEPTANCE_FAILED
```

---

# 六、Governance 对下游的约束

## 1. `governance_to_domain_constraints.yaml`

保存路径：

```text
00_governance/governance_to_domain_constraints.yaml
```

```yaml
constraint_id: GOVERNANCE_TO_DOMAIN_CONSTRAINTS_001
version: 20260511_governance_plane_v2

domain_plane_must_include:
  - domain_object_registry
  - domain_relation_graph
  - domain_decision_question_tree
  - scenario_taxonomy
  - wallet_role_taxonomy
  - dominant_side_lifecycle_taxonomy
  - evidence_requirement_model
  - contradiction_requirement_model

domain_language_rules:
  - dominant_side_intent_must_be_hypothesis
  - wallet_role_requires_evidence_level
  - scenario_requires_positive_and_negative_evidence
  - unknown_must_remain_unknown_if_evidence_missing

forbidden_domain_definitions:
  - deterministic_market_maker_identity_without_evidence
  - scenario_without_contradiction_rules
  - wallet_role_without_evidence_fields
  - strategy_permission_inside_domain_plane
```

---

## 2. `governance_to_data_constraints.yaml`

保存路径：

```text
00_governance/governance_to_data_constraints.yaml
```

```yaml
constraint_id: GOVERNANCE_TO_DATA_CONSTRAINTS_001
version: 20260511_governance_plane_v2

data_plane_must_include:
  - field_source_map
  - normalized_fact_model
  - data_input_contract
  - data_quality_rules
  - evidence_level_rules
  - contradiction_record_rules
  - missing_data_policy

field_governance_rules:
  - every_required_field_must_have_source
  - every_required_field_must_have_consumer_phase
  - every_required_field_must_have_missing_policy
  - every_blocking_field_must_be_marked
  - every_evidence_field_must_have_evidence_level
  - every_contradiction_field_must_be_recordable

forbidden_data_behavior:
  - infer_missing_core_field_without_source
  - silently_drop_missing_blocking_field
  - allow_p01_without_data_input_contract
  - allow_strategy_gate_read_raw_unstandardized_data
```

---

## 3. `governance_to_control_constraints.yaml`

保存路径：

```text
00_governance/governance_to_control_constraints.yaml
```

```yaml
constraint_id: GOVERNANCE_TO_CONTROL_CONSTRAINTS_001
version: 20260511_governance_plane_v2

control_plane_must_enforce:
  - p01_blocked_until_data_plane_acceptance
  - paper_runtime_blocked_until_p06_p07
  - real_trade_always_false
  - runner_must_not_bypass_phase_controller
  - review_must_not_directly_modify_rules

control_state_required_fields:
  - current_authoritative_stage
  - blocked_stages
  - block_reasons
  - next_legal_stage
  - p01_runtime_connection_allowed
  - paper_only
  - real_trade_enabled

conflict_policy_required:
  - current_system_state_highest_authority
  - blocked_status_wins_until_acceptance_passed
  - real_trade_true_forced_false
```

---

# 七、Governance 验收模型

## 1. `governance_readiness_gate.yaml`

保存路径：

```text
00_governance/governance_readiness_gate.yaml
```

```yaml
gate_id: GOVERNANCE_READINESS_GATE_001
version: 20260511_governance_plane_v2

readiness_result_values:
  - GOVERNANCE_READY
  - GOVERNANCE_WITH_WARNINGS
  - GOVERNANCE_BLOCKED
  - GOVERNANCE_FAILED

required_for_GOVERNANCE_READY:
  - governance_plane_md_exists
  - authority_boundary_exists
  - stage_permission_matrix_exists
  - hard_negative_rules_exists
  - risk_boundary_exists
  - real_trade_forbidden_policy_exists
  - review_to_upgrade_policy_exists
  - evidence_language_policy_exists
  - assumption_control_policy_exists
  - runner_permission_policy_exists
  - governance_to_domain_constraints_exists
  - governance_to_data_constraints_exists
  - governance_to_control_constraints_exists
  - paper_only_true
  - real_trade_enabled_false
  - p01_runtime_connection_allowed_false

warning_conditions:
  - schemas_exist_but_not_yet_validated_by_runner
  - event_log_empty_before_first_runtime
  - downstream_domain_not_yet_consumed
  - downstream_data_not_yet_consumed

blocking_conditions:
  - real_trade_forbidden_policy_missing
  - hard_negative_rules_missing
  - authority_boundary_missing
  - p01_allowed_before_data_plane
  - real_trade_enabled_true
```

---

## 2. `governance_validation_rules.yaml`

保存路径：

```text
00_governance/governance_validation_rules.yaml
```

```yaml
validation_id: GOVERNANCE_VALIDATION_RULES_001
version: 20260511_governance_plane_v2

file_validation:
  required_files:
    - governance_plane.md
    - authority_boundary.yaml
    - stage_permission_matrix.yaml
    - hard_negative_rules.yaml
    - risk_boundary.yaml
    - real_trade_forbidden_policy.yaml
    - review_to_upgrade_policy.yaml
    - evidence_language_policy.yaml
    - assumption_control_policy.yaml
    - runner_permission_policy.yaml
    - governance_to_domain_constraints.yaml
    - governance_to_data_constraints.yaml
    - governance_to_control_constraints.yaml

semantic_validation:
  required_conditions:
    - K00_cannot_start_P01
    - P00_cannot_start_P01
    - P01_cannot_generate_trade_signal
    - P06_can_only_allow_paper
    - P08_cannot_execute_real_trade
    - P09_cannot_modify_runtime_rules
    - P10_cannot_enable_real_trade
    - real_trade_forbidden_globally
    - evidence_language_required
    - assumptions_must_be_labeled

hard_fail_conditions:
  - real_trade_enabled_true
  - missing_real_trade_forbidden_policy
  - missing_hard_negative_rules
  - p01_runtime_connection_allowed_true
  - paper_runtime_allowed_without_P06_P07
  - review_direct_rule_write_allowed
```

---

## 3. `governance_integrity_manifest.json`

保存路径：

```text
00_governance/governance_integrity_manifest.json
```

```json
{
  "manifest_id": "GOVERNANCE_INTEGRITY_MANIFEST_20260511",
  "plane": "GOVERNANCE_PLANE",
  "version": "v2.0-institutional",

  "required_files": [
    "governance_plane.md",
    "authority_boundary.yaml",
    "stage_permission_matrix.yaml",
    "hard_negative_rules.yaml",
    "risk_boundary.yaml",
    "real_trade_forbidden_policy.yaml",
    "review_to_upgrade_policy.yaml",
    "evidence_language_policy.yaml",
    "assumption_control_policy.yaml",
    "exception_escalation_policy.yaml",
    "legacy_runtime_quarantine_policy.yaml",
    "runner_permission_policy.yaml",
    "governance_to_domain_constraints.yaml",
    "governance_to_data_constraints.yaml",
    "governance_to_control_constraints.yaml",
    "governance_readiness_gate.yaml",
    "governance_validation_rules.yaml"
  ],

  "schema_files": [
    "schemas/authority_boundary.schema.json",
    "schemas/stage_permission_matrix.schema.json",
    "schemas/hard_negative_rules.schema.json",
    "schemas/risk_boundary.schema.json",
    "schemas/governance_handoff_packet.schema.json"
  ],

  "governance_status": "GOVERNANCE_READY_PENDING_DOWNSTREAM_CONSUMPTION",

  "hard_safety_flags": {
    "paper_only": true,
    "real_trade_enabled": false,
    "auto_order_allowed": false,
    "p01_runtime_connection_allowed": false
  }
}
```

---

# 八、Governance Handoff

## 1. `governance_to_domain_handoff_packet.json`

保存路径：

```text
00_governance/governance_to_domain_handoff_packet.json
```

```json
{
  "handoff_id": "GOVERNANCE_TO_DOMAIN_HANDOFF_20260511",
  "source_stage": "GOVERNANCE_PLANE",
  "target_stage": "DOMAIN_PLANE",

  "included_assets": [
    "00_governance/authority_boundary.yaml",
    "00_governance/evidence_language_policy.yaml",
    "00_governance/assumption_control_policy.yaml",
    "00_governance/governance_to_domain_constraints.yaml"
  ],

  "domain_must_follow": [
    "wallet_role_requires_evidence_level",
    "dominant_side_intent_must_be_hypothesis",
    "scenario_requires_positive_and_negative_evidence",
    "unknown_must_remain_unknown_if_evidence_missing"
  ],

  "blocking_gaps": [],
  "non_blocking_gaps": [
    "Domain Plane not yet generated."
  ],

  "consumption_required": true,
  "p01_runtime_connection_allowed": false,

  "safety_boundary": {
    "paper_only": true,
    "real_trade_enabled": false
  }
}
```

---

## 2. `governance_to_data_handoff_packet.json`

保存路径：

```text
00_governance/governance_to_data_handoff_packet.json
```

```json
{
  "handoff_id": "GOVERNANCE_TO_DATA_HANDOFF_20260511",
  "source_stage": "GOVERNANCE_PLANE",
  "target_stage": "DATA_PLANE",

  "included_assets": [
    "00_governance/risk_boundary.yaml",
    "00_governance/hard_negative_rules.yaml",
    "00_governance/governance_to_data_constraints.yaml",
    "00_governance/assumption_control_policy.yaml"
  ],

  "data_must_follow": [
    "every_required_field_must_have_source",
    "every_required_field_must_have_consumer_phase",
    "every_required_field_must_have_missing_policy",
    "every_blocking_field_must_be_marked",
    "every_evidence_field_must_have_evidence_level"
  ],

  "blocking_gaps": [],
  "non_blocking_gaps": [
    "Data Plane not yet generated."
  ],

  "consumption_required": true,
  "p01_runtime_connection_allowed": false,

  "safety_boundary": {
    "paper_only": true,
    "real_trade_enabled": false
  }
}
```

---

# 九、Governance Event Log

## `governance_event_log.jsonl`

保存路径：

```text
00_governance/governance_event_log.jsonl
```

示例：

```json
{"event_id":"GOV_EVT_001","event_type":"GOVERNANCE_PLANE_CREATED","result":"governance_plane_v2_created","severity":"INFO"}
{"event_id":"GOV_EVT_002","event_type":"REAL_TRADE_FORBIDDEN_POLICY_CREATED","result":"real_trade_enabled_false_enforced","severity":"P0_CONTROL"}
{"event_id":"GOV_EVT_003","event_type":"STAGE_PERMISSION_MATRIX_CREATED","result":"stage_permissions_defined","severity":"INFO"}
{"event_id":"GOV_EVT_004","event_type":"HARD_NEGATIVE_RULES_CREATED","result":"hard_negative_rules_active","severity":"P0_CONTROL"}
{"event_id":"GOV_EVT_005","event_type":"GOVERNANCE_HANDOFF_READY","result":"governance_to_domain_and_data_handoff_created","severity":"INFO"}
```

---

# 十、Governance Plane 是否达到专业级？

如果只做这些文件：

```text
governance_plane.md
authority_boundary.yaml
hard_negative_rules.yaml
risk_boundary.yaml
real_trade_forbidden_policy.yaml
```

只能算：

```text
轻量治理雏形
```

还不够专业。

如果补齐：

```text
阶段权限矩阵
证据语言策略
假设控制策略
runner 权限策略
旧系统隔离策略
复盘升级策略
Governance → Domain / Data / Control 约束
readiness gate
validation rules
integrity manifest
handoff packet
event log
schema
```

才可以接近：

```text
轻量机构级 Governance Plane v2.0
```

---

# 十一、完成后的合法系统状态

Governance Plane 完成后，应更新为：

```json
{
  "governance_plane_status": "GOVERNANCE_READY_PENDING_DOWNSTREAM_CONSUMPTION",
  "p01_runtime_connection_allowed": false,
  "next_legal_stage": "DOMAIN_PLANE_PROFESSIONAL_GENERATION",
  "paper_only": true,
  "real_trade_enabled": false
}
```

注意：

```text
Governance Plane 完成后，仍然不能进入 P01。
```

下一步应该是：

```text
Domain Plane 专业化生成
```

或者如果你想一次性生成系统平面，则是：

```text
SYSTEM_PLANES_PROFESSIONAL_GENERATION_AND_ACCEPTANCE
```

---

# 十二、HER 正式任务书

```text
任务名称：
GOVERNANCE_PLANE_V2_PROFESSIONAL_COMPLETION

任务类型：
Governance Plane 专业机构化生成任务。
不是 P01 运行任务。
不是自动化交易任务。
不是真实交易任务。

目标：
建立 SIKK Stable Trader OS 的 Governance Plane v2.0。
该平面必须定义系统权限边界、阶段权限矩阵、硬否定规则、风险边界、真实交易禁用策略、复盘升级边界、证据语言策略、假设控制策略、runner 权限策略、旧系统隔离策略、Governance 到 Domain/Data/Control 的约束、验收门、完整性清单和下游 handoff。

必须创建目录：
/root/sikk-gmgn/sikk_stable_trader_os/00_governance/
/root/sikk-gmgn/sikk_stable_trader_os/00_governance/schemas/
/root/sikk-gmgn/sikk_stable_trader_os/00_governance/reports/

必须创建或更新文件：
1. 00_governance/governance_plane.md
2. 00_governance/authority_boundary.yaml
3. 00_governance/stage_permission_matrix.yaml
4. 00_governance/hard_negative_rules.yaml
5. 00_governance/risk_boundary.yaml
6. 00_governance/real_trade_forbidden_policy.yaml
7. 00_governance/review_to_upgrade_policy.yaml
8. 00_governance/evidence_language_policy.yaml
9. 00_governance/assumption_control_policy.yaml
10. 00_governance/exception_escalation_policy.yaml
11. 00_governance/legacy_runtime_quarantine_policy.yaml
12. 00_governance/runner_permission_policy.yaml
13. 00_governance/governance_to_domain_constraints.yaml
14. 00_governance/governance_to_data_constraints.yaml
15. 00_governance/governance_to_control_constraints.yaml
16. 00_governance/governance_readiness_gate.yaml
17. 00_governance/governance_validation_rules.yaml
18. 00_governance/governance_integrity_manifest.json
19. 00_governance/governance_to_domain_handoff_packet.json
20. 00_governance/governance_to_data_handoff_packet.json
21. 00_governance/governance_event_log.jsonl
22. 00_governance/reports/governance_plane_acceptance_report.json

必须创建 schema 文件：
1. 00_governance/schemas/authority_boundary.schema.json
2. 00_governance/schemas/stage_permission_matrix.schema.json
3. 00_governance/schemas/hard_negative_rules.schema.json
4. 00_governance/schemas/risk_boundary.schema.json
5. 00_governance/schemas/governance_handoff_packet.schema.json

核心要求：
1. Governance Plane 必须明确 paper_only=true。
2. Governance Plane 必须明确 real_trade_enabled=false。
3. Governance Plane 必须明确 P01 在 Data Plane 验收前不得运行。
4. K00 不能直接进入 P01。
5. P00 不能直接启动 P01。
6. P01 不能生成交易判断。
7. P06 只能允许 paper，不能允许真实交易。
8. P08 只能运行 paper trade，不能运行真实交易。
9. P09 只能提出复盘建议，不能直接修改实时规则。
10. P10 只能受控升级，不能启用真实交易。
11. 未知钱包不得强行分类。
12. 主导侧意图必须写成证据假设。
13. 单一指标不得直接给买点。
14. 缺少反证记录不得通过策略门禁。
15. runner 不得绕过 Phase Controller。
16. 旧脚本不得未经注册直接进入正式系统。
17. 复盘结果不得绕过 P10 直接修改规则。

禁止事项：
1. 禁止启动 P01。
2. 禁止运行 paper trading。
3. 禁止真实交易。
4. 禁止把 Governance Plane 完成解释为系统可运行 P01。
5. 禁止删除 legacy runtime。
6. 禁止只写说明文档，不写机器可读规则。
7. 禁止没有 hard_negative_rules 就标记 Governance Ready。
8. 禁止没有 real_trade_forbidden_policy 就标记 Governance Ready。
9. 禁止没有 Governance → Domain/Data handoff 就进入下游阶段。

验收标准：
1. 所有 required files 存在。
2. 所有 JSON 可解析。
3. 所有 YAML 可解析。
4. authority_boundary.yaml 定义 K00-P10 权限边界。
5. stage_permission_matrix.yaml 定义阶段权限。
6. hard_negative_rules.yaml 包含真实交易硬禁用、P01 绕过 Data Plane、paper runner 绕过 P06/P07、复盘直接改规则等硬否定。
7. risk_boundary.yaml 定义 system/data/wallet/market/execution/governance 风险域。
8. real_trade_forbidden_policy.yaml 明确 real_trade_enabled=false。
9. review_to_upgrade_policy.yaml 明确 P09 不能直接修改实时规则。
10. evidence_language_policy.yaml 明确主导侧意图只能是证据假设。
11. assumption_control_policy.yaml 明确缺失字段不得靠假设补齐。
12. runner_permission_policy.yaml 明确 runner 不得绕过 Phase Controller。
13. governance_to_domain_constraints.yaml 存在。
14. governance_to_data_constraints.yaml 存在。
15. governance_to_control_constraints.yaml 存在。
16. governance_readiness_gate.yaml 结果为 GOVERNANCE_READY 或 GOVERNANCE_WITH_WARNINGS。
17. governance_integrity_manifest.json 存在。
18. governance_to_domain_handoff_packet.json 存在。
19. governance_to_data_handoff_packet.json 存在。
20. p01_runtime_connection_allowed=false。
21. paper_only=true。
22. real_trade_enabled=false。

最终输出：
1. 创建文件清单。
2. 更新文件清单。
3. 备份文件清单。
4. Governance Plane 验收结果。
5. readiness gate 结果。
6. 当前治理状态。
7. 下一合法阶段。
8. 是否允许进入 P01：必须回答否。
```

---

# 十三、最终结论

专业级 `Governance Plane` 不只是“安全规则文档”。

它必须是：

```text
权限边界
阶段权限
硬否定规则
风险边界
真实交易禁用
证据语言控制
假设控制
runner 权限控制
旧系统隔离
复盘升级边界
Domain / Data / Control 约束
readiness gate
validation rules
integrity manifest
handoff packet
event log
```

补齐这些后，才可以认为：

```text
Governance Plane 达到轻量机构化专业水准。
```

但即使完成 Governance Plane，仍然不能进入 P01。

下一步应该是：

```text
Domain Plane 专业化生成
```

或者继续总任务：

```text
SYSTEM_PLANES_PROFESSIONAL_GENERATION_AND_ACCEPTANCE
```

---

# 本次认知升级点

```text
1. Governance Plane 不是规则说明，而是系统权限与风险裁决平面。

2. 专业治理平面必须同时约束阶段、runner、数据、领域语言、复盘升级和真实交易边界。

3. Governance Plane 必须向 Domain Plane 和 Data Plane 输出正式约束，否则下游仍会自由发挥。

4. 真实交易禁用必须作为独立 policy，不应只是口头说明。

5. 复盘结果不能直接改规则，必须进入 P10 受控升级。

6. 主导侧意图必须使用证据假设语言，防止 AI 把推断写成事实。

7. Governance Plane 完成后，仍然不能进入 P01。
```

# 尚未解决问题

```text
1. Governance Plane v2.0 是否已真实落盘？

2. authority_boundary.yaml 是否已覆盖 K00-P10？

3. stage_permission_matrix.yaml 是否已定义每个阶段的 can / cannot？

4. hard_negative_rules.yaml 是否已包含真实交易、P01 绕过 Data Plane、paper runner 绕过 P06/P07、复盘直接改规则等 P0 级硬否定？

5. evidence_language_policy.yaml 是否已限制“庄家一定”“必拉”等确定性语言？

6. assumption_control_policy.yaml 是否已禁止缺失字段靠推断补齐？

7. governance_to_domain_constraints.yaml 是否已成为 Domain Plane 输入？

8. governance_to_data_constraints.yaml 是否已成为 Data Plane 输入？

9. governance_integrity_manifest.json 是否已登记全部治理文件？

10. governance_readiness_gate 是否达到 GOVERNANCE_READY 或 GOVERNANCE_WITH_WARNINGS？

11. current_system_state.json 是否已更新 governance_plane_status？

12. P01 是否仍然被正确阻断？
```