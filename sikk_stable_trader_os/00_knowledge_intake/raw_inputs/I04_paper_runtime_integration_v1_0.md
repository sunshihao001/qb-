# I04 Paper-only Runtime Integration 专业版 v1.0

## 纸面运行联调、模拟仓位、模拟成交、滑点费用、退出事件、风险事件与 P09 复盘输入任务包

---

## 0. I04 的核心定位

I04 不是新的业务阶段，也不是 P14。

它属于：

```text
Integration Program：系统集成落地计划
```

I04 的专业定义：

```text
I04 Paper-only Runtime Integration 是在 I03 Runner / Tool Binding 完成后，把 P08 Execution Risk Controller 输出的 PAPER_RUNTIME_ALLOWED / PAPER_RUNTIME_ALLOWED_WITH_LIMITATIONS 候选，接入严格 paper-only 的运行系统，生成可追踪、可验收、可复盘、可归因的纸面仓位、纸面交易、权益曲线、运行事件、风险事件、退出事件和 P09 复盘输入。
```

一句话：

> **I03 解决“runner 和工具如何绑定”。**  
> **I04 解决“P08 允许的样本如何进入纸面运行，并产生可被 P09 回放的真实 runtime 记录”。**

---

# 1. I04 不能负责什么

I04 必须严格阻断以下行为：

```text
不新增 P11 / P12 / P13 / P14
不修改 P01-P10 业务逻辑
不重新判断场景
不重新判断策略
不绕过 P08
不接收 P07 直接输入
不真实下单
不钱包签名
不连接实盘交易权限
不自动 swap
不自动部署
不删除 legacy 数据
不把 legacy paper_live 当成当前 canonical runtime
不允许 live execution
```

I04 只做：

```text
读取 P08 handoff
读取 paper_runtime_permission
读取 paper_entry_simulation_plan
创建纸面仓位
记录纸面入场
应用滑点模型
应用费用模型
更新开放仓位
处理退出条件
记录退出事件
记录风险事件
生成权益曲线
生成 runtime trace
生成 runtime acceptance
生成 P09 review replay 输入
生成 I04→I05 handoff
```

---

# 2. I04 阶段目标

I04 必须一次性解决 22 类问题：

|编号|问题|I04 必须输出|
|---|---|---|
|1|P08 是否允许进入 paper runtime？|`p08_permission_ingestion_record`|
|2|Paper Runtime 如何读取 P08 handoff？|`paper_runtime_input_manifest`|
|3|如何防止 P07 绕过 P08？|`runtime_permission_gate_record`|
|4|如何创建纸面仓位？|`paper_position_open_record`|
|5|如何记录模拟入场？|`paper_trade_record`|
|6|如何应用有效入场价？|`paper_entry_price_model_record`|
|7|如何应用滑点？|`paper_slippage_application_record`|
|8|如何应用费用？|`paper_cost_application_record`|
|9|如何更新开放仓位？|`paper_position_update_record`|
|10|如何记录未实现盈亏？|`paper_mark_to_market_record`|
|11|如何处理退出条件？|`paper_exit_rule_evaluation_record`|
|12|如何记录退出事件？|`paper_exit_event_record`|
|13|如何关闭仓位？|`paper_position_close_record`|
|14|如何生成权益曲线？|`paper_equity_curve_record`|
|15|如何记录风险事件？|`paper_runtime_risk_event_record`|
|16|如何监控 P07/P08 失效条件？|`runtime_invalidation_monitor_record`|
|17|如何保证 one-token-one-position？|`paper_position_uniqueness_record`|
|18|如何处理重复信号 / 重复候选？|`paper_candidate_dedup_record`|
|19|如何记录 runtime trace？|`paper_runtime_trace_record`|
|20|如何验收 runtime 输出？|`paper_runtime_acceptance_result`|
|21|如何交给 P09 复盘？|`p09_review_replay_input_packet`|
|22|是否可以进入 I05 闭环回放？|`i04_to_i05_handoff_packet`|

---

# 3. I04 的底层方法论

## 3.1 Paper Runtime 不是玩具记录，而是仿真账本

普通纸面交易只记录：

```text
买入价
卖出价
收益率
```

专业 Paper Runtime 必须记录：

```text
为什么允许进入
谁允许进入
P08 permission 是什么
使用哪个 entry simulation plan
用哪个 quote
用哪个 effective entry price
滑点如何计算
费用如何计算
退出条件是什么
风险事件什么时候发生
失效条件是否触发
仓位状态如何变化
每次更新是否可追踪
P09 能否完整回放
```

---

## 3.2 I04 不能重新做策略判断

I04 不判断：

```text
这个币是不是二段扩张
筹码是否仍在主导侧
是否值得买
是否应该放行
```

这些由 P04-P08 完成。

I04 只判断：

```text
P08 已经允许的纸面样本，是否能按 paper-only runtime 规则被模拟、记录、更新、退出和复盘。
```

---

## 3.3 Paper-only 不等于无风控

即使是纸面，也必须风控。

I04 必须继承：

```text
P08 风控限制
P07 失效条件
P06 场景风险标签
P05 反证标签
P04 筹码风险标签
Governance 禁止事项
Path Guard
Trace / Acceptance / Handoff
```

否则纸面结果会变成“幻想收益”。

---

## 3.4 纸面收益必须净值化

I04 不能只记录 gross PnL。

必须同时记录：

```text
gross_pnl
slippage_cost
fee_cost
spread_cost
net_pnl
max_favorable_excursion
max_adverse_excursion
holding_duration
exit_reason
```

否则 P09 无法判断：

```text
策略有效
还是 paper 模型过度乐观
```

---

## 3.5 Runtime 输出必须服务 P09

I04 的最终目标不是“纸面看起来有收益”，而是：

```text
生成 P09 能重建决策链、运行链、入场、持仓、退出、风险、失败归因的数据。
```

所以 I04 的输出必须天然支持：

```text
decision_time_snapshot
entry_snapshot
update_snapshot
exit_snapshot
runtime_event_trace
risk_event_trace
p08_permission_trace
p07_invalidation_trace
```

---

# 4. I04 输入范围

```yaml
i04_required_inputs:
  from_i03:
    - i03_to_i04_handoff_packet
    - i04_paper_runtime_prerequisite_packet
    - phase_runner_binding_index
    - tool_binding_index
    - runner_cli_command_registry
    - environment_config_registry
    - path_guard_binding
    - schema_validator_binding
    - contract_validator_binding
    - trace_writer_binding
    - acceptance_runner_binding
    - handoff_writer_binding
    - runner_error_policy
    - dry_run_validation_report
    - i03_acceptance_result

  from_i02:
    - runtime_data_path_index
    - schema_index
    - contract_index
    - handoff_contract_index
    - read_order_manifest
    - write_permission_matrix
    - canonical_path_policy
    - legacy_path_mapping

  from_p08:
    - p08_to_paper_runtime_handoff_packet
    - paper_runtime_data_request_packet
    - paper_runtime_permission_records
    - paper_entry_simulation_plans
    - quote_snapshot_records
    - quote_consistency_records
    - liquidity_depth_records
    - slippage_estimation_records
    - execution_cost_model_records
    - security_recheck_records
    - sellability_risk_records
    - invalidation_precheck_records
    - runtime_risk_limit_records
    - position_uniqueness_records
    - circuit_breaker_records

  from_p07:
    - strategy_gate_decision_records
    - strategy_candidate_records
    - strategy_invalidation_binding_records
    - strategy_usage_permission_records

  from_runtime_state:
    - existing_open_paper_positions
    - existing_closed_paper_positions
    - existing_paper_trades
    - existing_equity_curve
    - existing_risk_events

  from_global_control:
    - forbidden_use_policy
    - global_hard_negative_rules
    - global_status_code_table
    - governance_handoff_packet
```

I04 启动前必须确认：

```text
I03 已验收
I03→I04 handoff 已生成
P08→Paper Runtime handoff 已存在
P08 permission 为 PAPER_RUNTIME_ALLOWED 或 PAPER_RUNTIME_ALLOWED_WITH_LIMITATIONS
Paper Runtime 不能接收 P07 直接输入
live execution 全局关闭
wallet signing 全局关闭
path guard 已启用
trace / acceptance / handoff writer 已启用
```

---

# 5. I04 必须建立的核心对象

|对象|作用|
|---|---|
|`Paper Runtime Input Manifest`|记录 I04 接收哪些 P08 / I03 输入|
|`P08 Permission Ingestion Record`|接收 P08 permission 并校验|
|`Runtime Permission Gate Record`|阻断无 P08 permission 的输入|
|`Paper Candidate Queue Record`|纸面候选队列|
|`Paper Candidate Dedup Record`|去重与重复信号处理|
|`Paper Position Uniqueness Record`|one-token-one-position 检查|
|`Paper Entry Price Model Record`|入场价格模型|
|`Paper Slippage Application Record`|滑点应用|
|`Paper Cost Application Record`|费用应用|
|`Paper Position Open Record`|开仓记录|
|`Paper Trade Record`|纸面交易记录|
|`Paper Position Update Record`|持仓更新|
|`Paper Mark To Market Record`|按当前价格估值|
|`Runtime Invalidation Monitor Record`|失效条件监控|
|`Paper Exit Rule Evaluation Record`|退出条件评估|
|`Paper Exit Event Record`|退出事件|
|`Paper Position Close Record`|关闭仓位|
|`Paper Equity Curve Record`|权益曲线|
|`Paper Runtime Risk Event Record`|风险事件|
|`Paper Runtime Snapshot Record`|runtime 快照|
|`Paper Runtime Trace Record`|runtime trace|
|`Paper Runtime Acceptance Result`|runtime 验收|
|`P09 Review Replay Input Packet`|P09 复盘输入包|
|`I04 to I05 Handoff Packet`|I04 → I05 闭环回放交接包|

---

# 6. I04 运行目录设计

## 6.1 系统目录

```text
/root/sikk-gmgn/system/integration_program/I04_paper_runtime_integration/
```

必须创建：

```text
i04_paper_runtime_integration_controller.yaml
i04_paper_runtime_integration_context.md
i04_input_contract.yaml
i04_output_contract.yaml
paper_runtime_input_manifest_schema.yaml
p08_permission_ingestion_schema.yaml
runtime_permission_gate_schema.yaml
paper_candidate_queue_schema.yaml
paper_candidate_dedup_schema.yaml
paper_position_uniqueness_schema.yaml
paper_entry_price_model_schema.yaml
paper_slippage_application_schema.yaml
paper_cost_application_schema.yaml
paper_position_open_schema.yaml
paper_trade_schema.yaml
paper_position_update_schema.yaml
paper_mark_to_market_schema.yaml
runtime_invalidation_monitor_schema.yaml
paper_exit_rule_evaluation_schema.yaml
paper_exit_event_schema.yaml
paper_position_close_schema.yaml
paper_equity_curve_schema.yaml
paper_runtime_risk_event_schema.yaml
paper_runtime_snapshot_schema.yaml
paper_runtime_trace_schema.yaml
paper_runtime_acceptance_result_schema.yaml
p09_review_replay_input_packet_contract.yaml
i04_to_i05_handoff_contract.yaml
paper_runtime_policy.yaml
paper_entry_policy.yaml
paper_update_policy.yaml
paper_exit_policy.yaml
paper_cost_slippage_policy.yaml
paper_risk_event_policy.yaml
paper_runtime_hard_negative_rules.yaml
paper_runtime_state_machine.yaml
paper_runtime_trace_requirements.yaml
i04_acceptance_criteria.md
i04_storage_constitution.md
i04_test_matrix.yaml
i04_report_model.yaml
i04_review_checklist.md
her_i04_execution_protocol.md
```

---

## 6.2 运行数据目录

```text
/root/sikk-gmgn/data/integration_program/I04_paper_runtime_integration/
  input_manifest/
  p08_permission_ingestion/
  runtime_permission_gate/
  candidate_queue/
  candidate_dedup/
  position_uniqueness/
  entry_price_model/
  slippage_application/
  cost_application/
  position_open/
  trades/
  position_updates/
  mark_to_market/
  invalidation_monitor/
  exit_rule_evaluation/
  exit_events/
  position_close/
  equity_curve/
  risk_events/
  runtime_snapshots/
  p09_review_inputs/
  i05_handoff/
  reports/
  audit/
  trace/
  acceptance/
```

正式 paper runtime canonical 目录：

```text
/root/sikk-gmgn/data/paper_runtime/
  positions_open/
  positions_closed/
  trades/
  equity_curve/
  runtime_events/
  exit_events/
  risk_events/
  snapshots/
  daily_reports/
  p09_review_inputs/
  trace/
  acceptance/
  handoff/
  reports/
  audit/
```

---

# 7. Paper Runtime Input Manifest

```yaml
paper_runtime_input_manifest:
  manifest_id: string
  generated_at: datetime

  upstream_packets:
    i03_to_i04_handoff_packet_id: string
    i04_prerequisite_packet_id: string
    p08_to_paper_runtime_handoff_packet_id: string
    paper_runtime_data_request_packet_id: string

  input_sources:
    p08_permission_records_path: string
    paper_entry_simulation_plans_path: string
    quote_snapshot_records_path: string
    slippage_estimation_records_path: string
    execution_cost_model_records_path: string
    invalidation_precheck_records_path: string
    strategy_invalidation_binding_records_path: string
    runtime_risk_limit_records_path: string

  input_quality:
    p08_handoff_valid: boolean
    i03_binding_valid: boolean
    path_guard_enabled: boolean
    trace_writer_enabled: boolean
    acceptance_runner_enabled: boolean
    handoff_writer_enabled: boolean
    runtime_input_quality_status:
      - RUNTIME_INPUT_HIGH_CONFIDENCE
      - RUNTIME_INPUT_USABLE
      - RUNTIME_INPUT_USABLE_WITH_GAPS
      - RUNTIME_INPUT_LOW_CONFIDENCE
      - RUNTIME_INPUT_UNUSABLE

  restrictions:
    paper_only: true
    live_execution_allowed: false
    wallet_signing_allowed: false
    auto_order_allowed: false
    p07_direct_input_allowed: false

  trace:
    input_manifest_trace_id: string
    upstream_trace_ids: list
```

---

# 8. P08 Permission Ingestion Record

```yaml
p08_permission_ingestion_record:
  ingestion_id: string
  candidate_id: string
  token_address: string
  generated_at: datetime

  p08_permission:
    permission_id: string
    final_permission:
      - PAPER_RUNTIME_ALLOWED
      - PAPER_RUNTIME_ALLOWED_WITH_LIMITATIONS
      - PAPER_RUNTIME_PAUSED
      - PAPER_RUNTIME_BLOCKED
      - HUMAN_CONFIRMATION_REQUIRED
      - EXECUTION_RISK_REJECTED

  ingestion_checks:
    permission_record_exists: boolean
    permission_allows_runtime: boolean
    permission_not_expired: boolean
    p08_trace_available: boolean
    p08_acceptance_valid: boolean
    paper_entry_simulation_plan_available: boolean
    live_execution_false: boolean
    wallet_signing_false: boolean

  ingestion_result:
    - ACCEPT_FOR_PAPER_QUEUE
    - ACCEPT_WITH_LIMITATIONS
    - REJECT_BLOCKED_BY_P08
    - PAUSE_WAIT_REFRESH
    - BLOCK_INVALID_PERMISSION
```

---

# 9. Runtime Permission Gate Record

```yaml
runtime_permission_gate_record:
  gate_id: string
  candidate_id: string

  gate_checks:
    came_from_p08_handoff: boolean
    has_valid_paper_runtime_permission: boolean
    p07_direct_bypass_absent: boolean
    strategy_candidate_valid: boolean
    p08_restrictions_preserved: boolean
    no_live_execution_path: boolean
    no_wallet_signing_path: boolean

  gate_result:
    - RUNTIME_GATE_ALLOWED
    - RUNTIME_GATE_ALLOWED_WITH_LIMITATIONS
    - RUNTIME_GATE_PAUSED
    - RUNTIME_GATE_BLOCKED

  block_reasons:
    - NO_P08_PERMISSION
    - P08_BLOCKED
    - P07_BYPASS_ATTEMPT
    - PERMISSION_EXPIRED
    - LIVE_EXECUTION_PATH_DETECTED
    - WALLET_SIGNING_PATH_DETECTED
```

---

# 10. Paper Candidate Queue Record

```yaml
paper_candidate_queue_record:
  queue_id: string
  generated_at: datetime

  queued_candidates:
    - candidate_id: string
      token_address: string
      p08_permission_id: string
      strategy_candidate_id: string
      queue_status:
        - QUEUED_FOR_OPEN
        - QUEUED_WITH_LIMITATIONS
        - QUEUED_FOR_REFRESH
        - REJECTED_FROM_QUEUE
      priority:
        - HIGH
        - MEDIUM
        - LOW
      limitation_tags: list

  queue_summary:
    total_received: integer
    queued_for_open_count: integer
    queued_with_limitations_count: integer
    rejected_count: integer
```

---

# 11. Paper Candidate Dedup Record

```yaml
paper_candidate_dedup_record:
  dedup_id: string
  candidate_id: string
  token_address: string

  duplicate_checks:
    same_candidate_already_queued: boolean
    same_token_already_open: boolean
    same_strategy_same_token_recently_closed: boolean
    repeated_permission_same_cycle: boolean

  dedup_action:
    - KEEP_NEW
    - MERGE_WITH_EXISTING_QUEUE_ITEM
    - IGNORE_DUPLICATE
    - BLOCK_EXISTING_OPEN_POSITION
    - REQUIRE_COOLDOWN

  reason_cn: string
```

---

# 12. Paper Position Uniqueness Record

```yaml
paper_position_uniqueness_record:
  uniqueness_id: string
  token_address: string
  candidate_id: string

  one_token_one_position_rule:
    enabled: true
    existing_open_position_id: string | null
    cooldown_active: boolean
    recent_closed_position_id: string | null

  uniqueness_result:
    - UNIQUE_ALLOWED
    - EXISTING_POSITION_BLOCKS
    - COOLDOWN_BLOCKS
    - STATE_REFRESH_REQUIRED

  downstream_effect:
    may_open_position: boolean
    reason_cn: string
```

---

# 13. Paper Entry Price Model Record

```yaml
paper_entry_price_model_record:
  entry_price_model_id: string
  candidate_id: string
  token_address: string

  source_prices:
    p08_reference_price_usd: number | null
    selected_quote_price_usd: number | null
    bid_price_usd: number | null
    ask_price_usd: number | null
    chain_estimated_price_usd: number | null

  entry_model:
    entry_mode:
      - PAPER_MARKET_SIMULATION
      - PAPER_LIMIT_SIMULATION
      - PAPER_MID_PRICE_SIMULATION
      - PAPER_CONFIRMATION_REQUIRED
    reference_price_usd: number
    effective_entry_price_before_cost_usd: number
    effective_entry_price_after_slippage_usd: number
    final_paper_entry_price_usd: number

  quality:
    quote_fresh: boolean
    quote_consistency_status: string
    entry_price_quality:
      - ENTRY_PRICE_HIGH_CONFIDENCE
      - ENTRY_PRICE_USABLE
      - ENTRY_PRICE_WITH_GAPS
      - ENTRY_PRICE_LOW_CONFIDENCE
      - ENTRY_PRICE_UNUSABLE
```

---

# 14. Paper Slippage Application Record

```yaml
paper_slippage_application_record:
  slippage_application_id: string
  candidate_id: string

  p08_slippage_inputs:
    slippage_estimation_id: string
    estimated_slippage_pct: number | null
    estimated_price_impact_pct: number | null
    worst_case_entry_price_usd: number | null

  applied_slippage:
    applied_slippage_pct: number
    applied_price_impact_pct: number
    slippage_cost_usd: number
    slippage_model:
      - P08_ESTIMATED
      - DEFAULT_CONSERVATIVE
      - ZERO_SLIPPAGE_WITH_WARNING
      - BLOCK_IF_UNKNOWN

  application_status:
    - SLIPPAGE_APPLIED
    - SLIPPAGE_APPLIED_WITH_LIMITATION
    - SLIPPAGE_MISSING_WITH_WARNING
    - SLIPPAGE_BLOCKED
```

---

# 15. Paper Cost Application Record

```yaml
paper_cost_application_record:
  cost_application_id: string
  candidate_id: string

  p08_cost_inputs:
    execution_cost_model_id: string
    estimated_network_fee_usd: number | null
    estimated_platform_fee_usd: number | null
    estimated_spread_cost_usd: number | null
    total_estimated_cost_usd: number | null

  applied_cost:
    network_fee_usd: number
    platform_fee_usd: number
    spread_cost_usd: number
    total_cost_usd: number
    total_cost_pct: number

  cost_policy:
    apply_fees: true
    apply_spread_cost: true
    apply_slippage_cost: true
    if_missing_cost_model:
      - APPLY_DEFAULT_CONSERVATIVE_COST
      - ALLOW_WITH_WARNING
      - BLOCK_RUNTIME

  application_status:
    - COST_APPLIED
    - COST_APPLIED_WITH_DEFAULTS
    - COST_MISSING_WITH_WARNING
    - COST_BLOCKED
```

---

# 16. Paper Position Open Record

```yaml
paper_position_open_record:
  paper_position_id: string
  candidate_id: string
  token_address: string
  opened_at: datetime

  upstream_basis:
    p08_permission_id: string
    p07_strategy_candidate_id: string
    strategy_profile_id: string
    paper_entry_simulation_plan_id: string

  entry:
    entry_price_usd: number
    reference_price_usd: number
    effective_entry_price_usd: number
    simulated_size_usd: number
    simulated_size_token: number
    slippage_application_id: string
    cost_application_id: string

  status:
    position_status:
      - OPEN
      - OPEN_WITH_LIMITATIONS
      - OPEN_REQUIRES_MONITORING

  inherited_monitoring:
    invalidation_binding_ids: list
    runtime_monitoring_requirements: list
    risk_tags: list
    limitation_tags: list

  restrictions:
    paper_only: true
    live_execution_allowed: false
    wallet_signing_allowed: false

  trace:
    open_trace_id: string
    source_trace_ids: list
```

---

# 17. Paper Trade Record

```yaml
paper_trade_record:
  trade_id: string
  paper_position_id: string
  candidate_id: string
  token_address: string
  trade_time: datetime

  trade:
    side:
      - PAPER_BUY
      - PAPER_SELL
    price_usd: number
    size_token: number
    notional_usd: number
    fee_usd: number
    slippage_cost_usd: number
    net_notional_usd: number

  source:
    trade_source:
      - PAPER_RUNTIME_ENTRY
      - PAPER_RUNTIME_EXIT
      - INVALIDATION_EXIT
      - RISK_EXIT
      - MANUAL_PAPER_EXIT

  trace:
    trade_trace_id: string
    source_trace_ids: list
```

---

# 18. Paper Position Update Record

```yaml
paper_position_update_record:
  update_id: string
  paper_position_id: string
  token_address: string
  updated_at: datetime

  market_snapshot:
    mark_price_usd: number
    mark_market_cap_usd: number | null
    liquidity_usd: number | null
    quote_freshness_status: string

  position_state:
    entry_price_usd: number
    current_price_usd: number
    size_token: number
    gross_unrealized_pnl_usd: number
    gross_unrealized_pnl_pct: number
    estimated_exit_cost_usd: number | null
    net_unrealized_pnl_usd: number | null
    net_unrealized_pnl_pct: number | null

  excursion:
    max_favorable_excursion_pct: number
    max_adverse_excursion_pct: number

  update_reason:
    - SCHEDULED_MARK
    - PRICE_REFRESH
    - RISK_CHECK
    - INVALIDATION_CHECK
    - EXIT_RULE_CHECK
```

---

# 19. Paper Mark To Market Record

```yaml
paper_mark_to_market_record:
  mtm_id: string
  generated_at: datetime

  positions:
    - paper_position_id: string
      token_address: string
      mark_price_usd: number
      gross_unrealized_pnl_pct: number
      net_unrealized_pnl_pct: number | null
      position_age_seconds: integer
      risk_status:
        - NORMAL
        - WATCH
        - RISK_WARNING
        - EXIT_REQUIRED
        - DATA_STALE

  portfolio_summary:
    open_position_count: integer
    total_gross_unrealized_pnl_usd: number
    total_net_unrealized_pnl_usd: number | null
    total_exposure_usd: number
```

---

# 20. Runtime Invalidation Monitor Record

```yaml
runtime_invalidation_monitor_record:
  invalidation_monitor_id: string
  paper_position_id: string
  candidate_id: string

  inherited_invalidations:
    - invalidation_id: string
      source_stage:
        - P06
        - P07
        - P08
      condition_cn: string
      severity:
        - HARD_INVALIDATION
        - SOFT_INVALIDATION
        - WATCH_INVALIDATION

  monitor_results:
    - invalidation_id: string
      checked_at: datetime
      triggered: boolean | null
      trigger_source: string | null
      detection_confidence:
        - HIGH
        - MEDIUM
        - LOW
        - UNKNOWN

  monitor_status:
    - NO_INVALIDATION
    - WATCH_INVALIDATION_TRIGGERED
    - SOFT_INVALIDATION_TRIGGERED
    - HARD_INVALIDATION_TRIGGERED
    - INVALIDATION_UNKNOWN_REFRESH_REQUIRED

  runtime_action:
    - CONTINUE_POSITION
    - WRITE_RISK_EVENT
    - EXIT_REQUIRED
    - PAUSE_UPDATE
    - REQUIRE_REFRESH
```

---

# 21. Paper Exit Rule Evaluation Record

```yaml
paper_exit_rule_evaluation_record:
  exit_eval_id: string
  paper_position_id: string
  candidate_id: string
  evaluated_at: datetime

  exit_rule_inputs:
    current_price_usd: number
    entry_price_usd: number
    net_unrealized_pnl_pct: number | null
    holding_duration_seconds: integer
    invalidation_monitor_status: string
    risk_event_status: string
    quote_freshness_status: string

  exit_rules_checked:
    - rule_id: STOP_LOSS
      triggered: boolean
    - rule_id: TAKE_PROFIT
      triggered: boolean
    - rule_id: HARD_INVALIDATION_EXIT
      triggered: boolean
    - rule_id: TIME_EXIT
      triggered: boolean
    - rule_id: DATA_STALE_PAUSE
      triggered: boolean
    - rule_id: SECURITY_RISK_EXIT
      triggered: boolean

  exit_decision:
    - HOLD
    - EXIT_REQUIRED
    - EXIT_RECOMMENDED
    - PAUSE_UNTIL_REFRESH
    - MANUAL_REVIEW_REQUIRED

  reason_cn: string
```

---

# 22. Paper Exit Event Record

```yaml
paper_exit_event_record:
  exit_event_id: string
  paper_position_id: string
  candidate_id: string
  token_address: string
  exit_time: datetime

  exit_basis:
    exit_reason:
      - TAKE_PROFIT
      - STOP_LOSS
      - HARD_INVALIDATION_TRIGGERED
      - SOFT_INVALIDATION_TRIGGERED
      - TIME_EXIT
      - SECURITY_RISK_EXIT
      - DATA_STALE_EXIT
      - MANUAL_PAPER_EXIT
    exit_rule_evaluation_id: string
    invalidation_monitor_id: string | null
    risk_event_ids: list

  exit_price:
    reference_exit_price_usd: number
    effective_exit_price_usd: number
    exit_slippage_pct: number
    exit_fee_usd: number

  trace:
    exit_trace_id: string
    source_trace_ids: list
```

---

# 23. Paper Position Close Record

```yaml
paper_position_close_record:
  close_id: string
  paper_position_id: string
  candidate_id: string
  token_address: string
  closed_at: datetime

  entry:
    entry_time: datetime
    entry_price_usd: number
    size_token: number
    entry_cost_usd: number

  exit:
    exit_time: datetime
    exit_price_usd: number
    exit_cost_usd: number
    exit_reason: string

  pnl:
    gross_pnl_usd: number
    gross_pnl_pct: number
    total_cost_usd: number
    total_slippage_cost_usd: number
    net_pnl_usd: number
    net_pnl_pct: number
    max_favorable_excursion_pct: number
    max_adverse_excursion_pct: number
    holding_duration_seconds: integer

  result_status:
    - WIN
    - LOSS
    - BREAKEVEN
    - INVALID
    - UNKNOWN

  p09_review_ready: boolean
  p09_review_input_packet_id: string | null
```

---

# 24. Paper Equity Curve Record

```yaml
paper_equity_curve_record:
  equity_curve_id: string
  generated_at: datetime

  equity_point:
    timestamp: datetime
    realized_pnl_usd: number
    unrealized_pnl_usd: number
    total_equity_usd: number
    open_position_count: integer
    closed_position_count: integer
    cumulative_return_pct: number
    drawdown_pct: number | null

  source:
    closed_positions_included: list
    open_positions_marked: list
    paper_trades_included: list
```

---

# 25. Paper Runtime Risk Event Record

```yaml
paper_runtime_risk_event_record:
  risk_event_id: string
  paper_position_id: string | null
  candidate_id: string | null
  token_address: string | null
  occurred_at: datetime

  risk_event_type:
    - HARD_INVALIDATION_TRIGGERED
    - SOFT_INVALIDATION_TRIGGERED
    - QUOTE_STALE
    - LIQUIDITY_DROPPED
    - SECURITY_RISK_REFRESHED
    - POSITION_DUPLICATE_ATTEMPT
    - PATH_GUARD_BLOCK
    - TRACE_WRITE_FAILURE
    - ACCEPTANCE_FAILURE
    - CIRCUIT_BREAKER_WARNING
    - PAPER_RUNTIME_BLOCKED
    - LIVE_EXECUTION_ATTEMPT_BLOCKED

  severity:
    - INFO
    - WARNING
    - HIGH
    - CRITICAL

  action_taken:
    - LOG_ONLY
    - POSITION_WATCH
    - EXIT_POSITION
    - BLOCK_NEW_POSITION
    - PAUSE_RUNTIME
    - HARD_BLOCK

  source_record_ids: list
  trace_id: string
```

---

# 26. Paper Runtime Snapshot Record

```yaml
paper_runtime_snapshot_record:
  snapshot_id: string
  generated_at: datetime

  snapshot_type:
    - ENTRY_SNAPSHOT
    - UPDATE_SNAPSHOT
    - EXIT_SNAPSHOT
    - DAILY_SNAPSHOT
    - REVIEW_SNAPSHOT

  included_data:
    open_positions_path: string
    closed_positions_path: string
    trades_path: string
    equity_curve_path: string
    runtime_events_path: string
    risk_events_path: string
    p08_permissions_path: string
    p07_decisions_path: string

  p09_replay_usage:
    decision_time_snapshot_available: boolean
    entry_snapshot_available: boolean
    exit_snapshot_available: boolean
    runtime_trace_available: boolean
```

---

# 27. P09 Review Replay Input Packet

```yaml
p09_review_replay_input_packet:
  packet_id: string
  packet_type: P09_REVIEW_REPLAY_INPUT_PACKET
  generated_at: datetime

  from: I04_PAPER_RUNTIME_INTEGRATION
  to: P09_REVIEW_REPLAY_CONTROLLER

  review_scope:
    paper_position_ids: list
    candidate_ids: list
    token_addresses: list
    review_trigger:
      - POSITION_OPENED
      - POSITION_CLOSED
      - RISK_EVENT_TRIGGERED
      - DAILY_REVIEW
      - MANUAL_REVIEW

  runtime_outputs:
    open_positions_path: string
    closed_positions_path: string
    paper_trades_path: string
    equity_curve_path: string
    runtime_events_path: string
    exit_events_path: string
    risk_events_path: string
    runtime_snapshots_path: string
    runtime_trace_path: string

  upstream_decision_context:
    p08_permission_records_path: string
    p07_strategy_gate_decision_records_path: string
    p06_scenario_records_path: string
    p05_evidence_records_path: string
    p04_chip_structure_records_path: string
    p03_wallet_entity_records_path: string
    p02_fact_records_path: string
    p01_candidate_records_path: string

  replay_requirements:
    lock_decision_time_snapshot: true
    distinguish_entry_snapshot_from_review_snapshot: true
    preserve_cost_and_slippage: true
    preserve_invalidation_events: true
    preserve_risk_events: true

  restrictions:
    p09_review_only: true
    no_direct_rule_mutation: true
    no_runtime_mutation: true
    no_live_execution: true
```

---

# 28. I04 to I05 Handoff Packet

```yaml
i04_to_i05_handoff_packet:
  packet_id: string
  packet_type: I04_TO_I05_PAPER_RUNTIME_HANDOFF
  generated_at: datetime

  route:
    from: I04_PAPER_RUNTIME_INTEGRATION
    to: I05_REVIEW_UPGRADE_CLOSED_LOOP

  upstream_control:
    i03_handoff_packet_id: string
    i04_acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    handoff_trace_id: string

  package_paths:
    paper_runtime_input_manifest_path: string
    p08_permission_ingestion_records_path: string
    runtime_permission_gate_records_path: string
    paper_candidate_queue_records_path: string
    paper_candidate_dedup_records_path: string
    paper_position_uniqueness_records_path: string
    paper_position_open_records_path: string
    paper_trade_records_path: string
    paper_position_update_records_path: string
    paper_mark_to_market_records_path: string
    runtime_invalidation_monitor_records_path: string
    paper_exit_rule_evaluation_records_path: string
    paper_exit_event_records_path: string
    paper_position_close_records_path: string
    paper_equity_curve_records_path: string
    paper_runtime_risk_event_records_path: string
    paper_runtime_snapshot_records_path: string
    p09_review_replay_input_packet_path: string
    i04_report_path: string

  i05_required_tasks:
    - run_p09_review_replay_on_i04_outputs
    - verify_decision_chain_reconstruction
    - verify_runtime_path_reconstruction
    - verify_failure_or_success_attribution
    - run_p10_upgrade_candidate_review
    - validate_closed_loop_trace
    - validate_p09_p10_handoff

  permission_to_enter_i05:
    - ALLOWED
    - ALLOWED_WITH_GAPS
    - BLOCKED_UNTIL_FIX

  restrictions:
    - I04_PAPER_ONLY_RUNTIME
    - I05_REVIEW_REPLAY_ONLY
    - NO_LIVE_EXECUTION
    - NO_WALLET_SIGNING
    - NO_AUTO_DEPLOY
```

---

# 29. I04 Gap Policy

```yaml
i04_gap_policy:
  BLOCKING_GAP:
    result: I04_BLOCKED
    examples:
      - i03_handoff_missing
      - p08_handoff_missing
      - p08_permission_missing
      - path_guard_missing
      - trace_writer_missing
      - live_execution_path_detected
      - wallet_signing_detected
      - paper_runtime_writes_unregistered_path

  CRITICAL_GAP:
    result: I04_REJECTED_OR_FIX_REQUIRED
    examples:
      - paper_position_schema_missing
      - paper_trade_schema_missing
      - paper_runtime_acceptance_missing
      - p09_review_input_packet_missing
      - p08_permission_gate_unusable
      - no_cost_or_slippage_policy

  HIGH_GAP:
    result: I04_READY_WITH_GAPS
    examples:
      - slippage_model_default_used
      - cost_model_default_used
      - exit_rule_partial
      - risk_event_model_partial
      - runtime_snapshot_partial

  MEDIUM_GAP:
    result: I04_READY_WITH_GAPS
    examples:
      - optional_daily_report_missing
      - noncritical_runtime_event_missing
      - legacy_comparison_missing

  LOW_GAP:
    result: I04_READY_WITH_NOTE
    examples:
      - optional_metadata_missing
      - noncritical_report_format_gap
```

---

# 30. I04 Hard Negative Rules

```yaml
i04_hard_negative_rules:
  - rule_id: I04_BLOCK_001
    name: 未读取 I03 handoff
    condition: i03_to_i04_handoff_packet_missing == true
    result: I04_BLOCKED
    reason: I04 必须基于 I03 绑定结果运行

  - rule_id: I04_BLOCK_002
    name: 未读取 P08 handoff
    condition: p08_to_paper_runtime_handoff_packet_missing == true
    result: I04_BLOCKED
    reason: Paper Runtime 不能绕过 P08

  - rule_id: I04_BLOCK_003
    name: P08 permission 缺失
    condition: paper_runtime_permission_missing == true
    result: I04_BLOCKED
    reason: 无 P08 许可不能创建纸面仓位

  - rule_id: I04_BLOCK_004
    name: P07 直接进入 Paper Runtime
    condition: direct_p07_input_detected == true
    result: I04_BLOCKED
    reason: P07 只能进入 P08，不能直接进入 Paper Runtime

  - rule_id: I04_BLOCK_005
    name: 创建真实订单
    condition: live_order_created == true
    result: I04_BLOCKED
    reason: I04 只允许 paper-only runtime

  - rule_id: I04_BLOCK_006
    name: 钱包签名路径
    condition: wallet_signing_detected == true
    result: I04_BLOCKED
    reason: I04 不能签名或调用真实钱包

  - rule_id: I04_BLOCK_007
    name: 未登记路径写入
    condition: unregistered_write_path_detected == true
    result: I04_BLOCKED
    reason: runtime 输出必须写入 canonical paper_runtime 路径

  - rule_id: I04_BLOCK_008
    name: 重复 token 开仓
    condition: one_token_one_position_violation == true
    result: I04_BLOCKED
    reason: paper runtime 必须执行单 token 单仓位规则

  - rule_id: I04_BLOCK_009
    name: 不记录 trace
    condition: runtime_trace_missing == true
    result: I04_BLOCKED
    reason: 无 trace 无法给 P09 回放

  - rule_id: I04_BLOCK_010
    name: 无 P09 review input
    condition: p09_review_input_packet_missing == true
    result: I04_BLOCKED
    reason: I04 必须产生 P09 可复盘输入
```

---

# 31. I04 状态机

```yaml
i04_paper_runtime_integration_state_machine:
  states:
    - I04_UNINITIALIZED
    - I04_CONTEXT_LOADED
    - I04_I03_HANDOFF_READ
    - I04_P08_HANDOFF_READ
    - I04_INPUT_MANIFEST_BUILT
    - I04_P08_PERMISSION_INGESTED
    - I04_RUNTIME_PERMISSION_GATE_CHECKED
    - I04_CANDIDATE_QUEUE_BUILT
    - I04_CANDIDATE_DEDUP_CHECKED
    - I04_POSITION_UNIQUENESS_CHECKED
    - I04_ENTRY_PRICE_MODEL_BUILT
    - I04_SLIPPAGE_APPLIED
    - I04_COST_APPLIED
    - I04_POSITION_OPENED
    - I04_TRADE_RECORDED
    - I04_POSITION_UPDATED
    - I04_MARK_TO_MARKET_BUILT
    - I04_INVALIDATION_MONITORED
    - I04_EXIT_RULES_EVALUATED
    - I04_EXIT_EVENTS_BUILT
    - I04_POSITIONS_CLOSED
    - I04_EQUITY_CURVE_UPDATED
    - I04_RISK_EVENTS_WRITTEN
    - I04_RUNTIME_SNAPSHOTS_BUILT
    - I04_P09_REVIEW_INPUT_BUILT
    - I04_REPORT_BUILT
    - I04_I05_HANDOFF_BUILT
    - I04_READY_FOR_ACCEPTANCE
    - I04_ACCEPTANCE_READY
    - I04_READY_FOR_I05_HANDOFF
    - I04_READY_WITH_GAPS
    - I04_REJECTED
    - I04_BLOCKED

  critical_transitions:
    - from: I04_CONTEXT_LOADED
      to: I04_I03_HANDOFF_READ
      condition: i03_to_i04_handoff_packet_available == true

    - from: I04_I03_HANDOFF_READ
      to: I04_P08_HANDOFF_READ
      condition: p08_to_paper_runtime_handoff_packet_available == true

    - from: I04_P08_HANDOFF_READ
      to: I04_INPUT_MANIFEST_BUILT
      condition: paper_runtime_input_manifest_created == true

    - from: I04_INPUT_MANIFEST_BUILT
      to: I04_P08_PERMISSION_INGESTED
      condition: p08_permission_ingestion_records_created == true

    - from: I04_P08_PERMISSION_INGESTED
      to: I04_RUNTIME_PERMISSION_GATE_CHECKED
      condition: runtime_permission_gate_records_created == true

    - from: I04_RUNTIME_PERMISSION_GATE_CHECKED
      to: I04_CANDIDATE_QUEUE_BUILT
      condition: allowed_candidates_queued == true

    - from: I04_CANDIDATE_QUEUE_BUILT
      to: I04_POSITION_UNIQUENESS_CHECKED
      condition: candidate_dedup_and_uniqueness_checked == true

    - from: I04_POSITION_UNIQUENESS_CHECKED
      to: I04_ENTRY_PRICE_MODEL_BUILT
      condition: entry_price_model_records_created == true

    - from: I04_ENTRY_PRICE_MODEL_BUILT
      to: I04_SLIPPAGE_APPLIED
      condition: slippage_application_records_created == true

    - from: I04_SLIPPAGE_APPLIED
      to: I04_COST_APPLIED
      condition: cost_application_records_created == true

    - from: I04_COST_APPLIED
      to: I04_POSITION_OPENED
      condition: paper_position_open_records_created == true

    - from: I04_POSITION_OPENED
      to: I04_TRADE_RECORDED
      condition: paper_trade_records_created == true

    - from: I04_TRADE_RECORDED
      to: I04_POSITION_UPDATED
      condition: paper_position_update_records_created == true

    - from: I04_POSITION_UPDATED
      to: I04_INVALIDATION_MONITORED
      condition: invalidation_monitor_records_created == true

    - from: I04_INVALIDATION_MONITORED
      to: I04_EXIT_RULES_EVALUATED
      condition: exit_rule_evaluation_records_created == true

    - from: I04_EXIT_RULES_EVALUATED
      to: I04_P09_REVIEW_INPUT_BUILT
      condition: p09_review_replay_input_packet_created == true

    - from: I04_P09_REVIEW_INPUT_BUILT
      to: I04_I05_HANDOFF_BUILT
      condition: i04_to_i05_handoff_packet_created == true

    - from: I04_I05_HANDOFF_BUILT
      to: I04_READY_FOR_ACCEPTANCE
      condition: i04_report_created == true
```

---

# 32. I04 Acceptance Criteria

```yaml
i04_acceptance_criteria:
  I04_READY:
    required:
      - i03_handoff_read
      - p08_handoff_read
      - paper_runtime_input_manifest_created
      - p08_permission_ingestion_created
      - runtime_permission_gate_created
      - candidate_queue_created
      - candidate_dedup_created
      - position_uniqueness_checked
      - entry_price_model_created
      - slippage_application_created
      - cost_application_created
      - paper_position_open_record_created
      - paper_trade_record_created
      - paper_position_update_record_created
      - mark_to_market_record_created
      - invalidation_monitor_created
      - exit_rule_evaluation_created
      - exit_event_or_hold_decision_recorded
      - equity_curve_created
      - risk_event_recording_enabled
      - runtime_snapshot_created
      - p09_review_input_packet_created
      - i04_to_i05_handoff_created
      - no_p07_bypass
      - no_live_execution
      - no_wallet_signing
      - no_unregistered_write_path

  I04_READY_WITH_GAPS:
    allowed_when:
      - slippage_default_used_with_warning
      - cost_model_default_used_with_warning
      - exit_model_partial_but_recorded
      - optional_daily_report_missing
    required:
      - gaps_recorded
      - p09_review_input_created
      - no_blocking_gap

  I04_REJECTED:
    triggered_by:
      - p08_permission_unusable
      - paper_runtime_schema_unusable
      - p09_review_input_unusable
      - cost_and_slippage_model_completely_missing
      - runtime_outputs_untraceable

  I04_BLOCKED:
    triggered_by:
      - missing_i03_handoff
      - missing_p08_handoff
      - missing_p08_permission
      - direct_p07_input_detected
      - live_execution_path_detected
      - wallet_signing_detected
      - unregistered_write_path_detected
      - runtime_trace_missing
      - p09_review_input_packet_missing
```

---

# 33. I04 测试矩阵

```yaml
i04_test_matrix:
  - test_id: I04_TEST_001
    name: P08 PAPER_RUNTIME_ALLOWED，完整 entry plan，创建纸面仓位
    expected_status: I04_READY

  - test_id: I04_TEST_002
    name: 缺 I03 handoff
    expected_status: I04_BLOCKED

  - test_id: I04_TEST_003
    name: 缺 P08 handoff
    expected_status: I04_BLOCKED

  - test_id: I04_TEST_004
    name: P08 permission 为 PAPER_RUNTIME_BLOCKED
    expected_status: I04_BLOCKED

  - test_id: I04_TEST_005
    name: P07 直接传入 PAPER_CANDIDATE
    expected_status: I04_BLOCKED

  - test_id: I04_TEST_006
    name: 已存在同 token 开放仓位
    expected_status: I04_BLOCKED

  - test_id: I04_TEST_007
    name: slippage model 缺失但 policy 允许默认保守模型
    expected_status: I04_READY_WITH_GAPS

  - test_id: I04_TEST_008
    name: cost model 缺失且 policy 要求阻断
    expected_status: I04_BLOCKED

  - test_id: I04_TEST_009
    name: 创建 paper trade 但未写 trace
    expected_status: I04_BLOCKED

  - test_id: I04_TEST_010
    name: runtime 输出写入未登记路径
    expected_status: I04_BLOCKED

  - test_id: I04_TEST_011
    name: hard invalidation 触发后记录 exit event
    expected_status: I04_READY

  - test_id: I04_TEST_012
    name: quote stale，退出规则要求 pause refresh
    expected_status: I04_READY_WITH_GAPS_OR_PAUSED

  - test_id: I04_TEST_013
    name: paper position close 后生成 P09 review input
    expected_status: I04_READY

  - test_id: I04_TEST_014
    name: 权益曲线没有包含 closed position
    expected_status: I04_READY_WITH_GAPS_OR_REJECTED

  - test_id: I04_TEST_015
    name: risk event 触发但未记录
    expected_status: I04_REJECTED

  - test_id: I04_TEST_016
    name: wallet signing path detected
    expected_status: I04_BLOCKED

  - test_id: I04_TEST_017
    name: live execution command detected
    expected_status: I04_BLOCKED

  - test_id: I04_TEST_018
    name: P09 review input packet 缺失
    expected_status: I04_BLOCKED

  - test_id: I04_TEST_019
    name: paper runtime snapshot 缺失但其他输出完整
    expected_status: I04_READY_WITH_GAPS

  - test_id: I04_TEST_020
    name: allowed_with_limitations 正确继承 limitation tags
    expected_status: I04_READY
```

---

# 34. I04 报告模型

```yaml
i04_paper_runtime_integration_report:
  report_id: string
  generated_at: datetime
  controller_id: I04_PAPER_RUNTIME_INTEGRATION

  summary:
    candidates_received_from_p08: integer
    candidates_accepted_to_queue: integer
    candidates_rejected: integer
    positions_opened: integer
    positions_updated: integer
    positions_closed: integer
    trades_recorded: integer
    risk_events_recorded: integer
    p09_review_packets_created: integer

  permission_summary:
    allowed_count: integer
    allowed_with_limitations_count: integer
    blocked_by_permission_count: integer
    paused_count: integer
    direct_p07_bypass_detected: boolean

  runtime_summary:
    open_positions_count: integer
    closed_positions_count: integer
    total_gross_pnl_usd: number
    total_net_pnl_usd: number
    total_fees_usd: number
    total_slippage_cost_usd: number
    win_count: integer
    loss_count: integer
    breakeven_count: integer

  model_summary:
    slippage_model_applied_count: integer
    default_slippage_used_count: integer
    cost_model_applied_count: integer
    default_cost_used_count: integer
    exit_rules_evaluated_count: integer
    invalidation_checks_count: integer

  risk_summary:
    hard_invalidation_exit_count: integer
    soft_invalidation_event_count: integer
    quote_stale_event_count: integer
    liquidity_drop_event_count: integer
    path_guard_block_count: integer
    duplicate_position_block_count: integer

  p09_readiness:
    p09_review_input_packet_created: boolean
    decision_time_snapshot_available: boolean
    runtime_trace_available: boolean
    entry_exit_records_available: boolean
    cost_slippage_records_available: boolean

  i05_readiness:
    i04_to_i05_handoff_created: boolean
    permission_to_enter_i05: string
    reasons_if_blocked: list

  compliance:
    live_execution_path_detected: false
    wallet_signing_detected: false
    p07_bypass_detected: false
    unregistered_write_path_detected: false
    legacy_write_detected: false
```

---

# 35. HER I04 执行协议

```text
HER 执行 I04 时必须按以下顺序：

1. 读取 system_methodology_blueprint.md
2. 读取 professional_build_order.md
3. 读取 I03→I04 handoff packet
4. 读取 I04 prerequisite packet
5. 读取 P08→Paper Runtime handoff packet
6. 读取 paper_runtime_data_request_packet
7. 读取 runtime_data_path_index
8. 读取 path_guard_binding
9. 读取 trace_writer_binding
10. 读取 acceptance_runner_binding
11. 读取 handoff_writer_binding
12. 读取 P08 permission records
13. 读取 paper_entry_simulation_plans
14. 读取 quote / slippage / cost / invalidation / risk limit records
15. 建立 paper_runtime_input_manifest
16. 建立 p08_permission_ingestion_records
17. 执行 runtime_permission_gate
18. 建立 paper_candidate_queue
19. 执行 candidate dedup
20. 执行 position uniqueness check
21. 建立 entry price model
22. 应用 slippage model
23. 应用 cost model
24. 创建 paper_position_open_record
25. 创建 paper_trade_record
26. 写入 open positions
27. 执行 mark-to-market 更新
28. 执行 invalidation monitor
29. 执行 exit rule evaluation
30. 如触发退出，生成 exit event 与 close record
31. 更新 equity curve
32. 写入 risk events
33. 生成 runtime snapshots
34. 写入 runtime trace
35. 运行 paper runtime acceptance
36. 生成 P09 review replay input packet
37. 生成 I04 paper runtime integration report
38. 生成 I04→I05 handoff packet
39. 生成 I04 acceptance result
40. 只允许 handoff 给 I05
```

禁止：

```text
1. 不允许无 I03 handoff 启动 I04
2. 不允许无 P08 handoff 启动 Paper Runtime
3. 不允许 P07 直接进入 Paper Runtime
4. 不允许真实下单
5. 不允许钱包签名
6. 不允许自动 swap
7. 不允许写入未登记路径
8. 不允许写入 legacy runtime path
9. 不允许忽略 slippage / cost
10. 不允许忽略 invalidation
11. 不允许无 trace 生成 paper trade
12. 不允许无 P09 review input 结束 I04
13. 不允许 live execution
```

---

# 36. 给 HER 的正式任务书

```text
任务名称：I04 Paper-only Runtime Integration：纸面运行联调任务包

目标：
在 /root/sikk-gmgn/system/integration_program/I04_paper_runtime_integration/ 下建立 I04 Paper-only Runtime Integration 任务包，并在 /root/sikk-gmgn/data/integration_program/I04_paper_runtime_integration/ 与 /root/sikk-gmgn/data/paper_runtime/ 下生成纸面运行输出。I04 不是 P14，不新增业务判断能力，不修改 P01-P10 业务逻辑。它的目标是在 I03 Runner / Tool Binding 完成后，把 P08 Execution Risk Controller 输出的 PAPER_RUNTIME_ALLOWED / PAPER_RUNTIME_ALLOWED_WITH_LIMITATIONS 候选接入严格 paper-only 的 runtime，生成可追踪、可验收、可回放、可归因的纸面仓位、纸面交易、权益曲线、风险事件、退出事件、runtime snapshot 和 P09 Review Replay 输入。

核心原则：
1. I04 是 Integration Program 第四步，不是新业务阶段。
2. I04 只做 Paper-only Runtime Integration。
3. I04 不重新判断策略。
4. I04 不重新判断场景。
5. I04 不修改 P01-P10 业务逻辑。
6. I04 不允许 P07 直接进入 Paper Runtime。
7. I04 必须读取 P08→Paper Runtime handoff。
8. I04 必须读取 paper_runtime_permission_records。
9. I04 必须应用 entry simulation plan。
10. I04 必须应用 slippage model。
11. I04 必须应用 cost model。
12. I04 必须记录 paper position open / update / close。
13. I04 必须记录 paper trades。
14. I04 必须记录 equity curve。
15. I04 必须记录 risk events。
16. I04 必须监控 invalidation conditions。
17. I04 必须生成 runtime snapshots。
18. I04 必须生成 P09 review replay input packet。
19. I04 必须生成 I04→I05 handoff packet。
20. I04 必须全局阻断 live execution、wallet signing、auto order。
21. I04 只能交接给 I05 Review / Upgrade Closed Loop。

需要创建系统目录：
/root/sikk-gmgn/system/integration_program/I04_paper_runtime_integration/

需要创建系统文件：
1. i04_paper_runtime_integration_controller.yaml
2. i04_paper_runtime_integration_context.md
3. i04_input_contract.yaml
4. i04_output_contract.yaml
5. paper_runtime_input_manifest_schema.yaml
6. p08_permission_ingestion_schema.yaml
7. runtime_permission_gate_schema.yaml
8. paper_candidate_queue_schema.yaml
9. paper_candidate_dedup_schema.yaml
10. paper_position_uniqueness_schema.yaml
11. paper_entry_price_model_schema.yaml
12. paper_slippage_application_schema.yaml
13. paper_cost_application_schema.yaml
14. paper_position_open_schema.yaml
15. paper_trade_schema.yaml
16. paper_position_update_schema.yaml
17. paper_mark_to_market_schema.yaml
18. runtime_invalidation_monitor_schema.yaml
19. paper_exit_rule_evaluation_schema.yaml
20. paper_exit_event_schema.yaml
21. paper_position_close_schema.yaml
22. paper_equity_curve_schema.yaml
23. paper_runtime_risk_event_schema.yaml
24. paper_runtime_snapshot_schema.yaml
25. paper_runtime_trace_schema.yaml
26. paper_runtime_acceptance_result_schema.yaml
27. p09_review_replay_input_packet_contract.yaml
28. i04_to_i05_handoff_contract.yaml
29. paper_runtime_policy.yaml
30. paper_entry_policy.yaml
31. paper_update_policy.yaml
32. paper_exit_policy.yaml
33. paper_cost_slippage_policy.yaml
34. paper_risk_event_policy.yaml
35. paper_runtime_hard_negative_rules.yaml
36. paper_runtime_state_machine.yaml
37. paper_runtime_trace_requirements.yaml
38. i04_acceptance_criteria.md
39. i04_storage_constitution.md
40. i04_test_matrix.yaml
41. i04_report_model.yaml
42. i04_review_checklist.md
43. her_i04_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/integration_program/I04_paper_runtime_integration/
  input_manifest/
  p08_permission_ingestion/
  runtime_permission_gate/
  candidate_queue/
  candidate_dedup/
  position_uniqueness/
  entry_price_model/
  slippage_application/
  cost_application/
  position_open/
  trades/
  position_updates/
  mark_to_market/
  invalidation_monitor/
  exit_rule_evaluation/
  exit_events/
  position_close/
  equity_curve/
  risk_events/
  runtime_snapshots/
  p09_review_inputs/
  i05_handoff/
  reports/
  audit/
  trace/
  acceptance/

需要创建或确认 canonical paper runtime 目录：
/root/sikk-gmgn/data/paper_runtime/
  positions_open/
  positions_closed/
  trades/
  equity_curve/
  runtime_events/
  exit_events/
  risk_events/
  snapshots/
  daily_reports/
  p09_review_inputs/
  trace/
  acceptance/
  handoff/
  reports/
  audit/

每个文件要求：
- i04_paper_runtime_integration_controller.yaml：定义 I04 身份、职责、权限、上下游、状态码、禁止事项。
- i04_paper_runtime_integration_context.md：写成 HER 执行前必须读取的 I04 上下文。
- i04_input_contract.yaml：定义 I04 必须读取的 I03 handoff、P08 handoff、P08 permission、entry plan、quote、slippage、cost、invalidation、risk limit。
- i04_output_contract.yaml：定义 paper position、trade、equity curve、risk event、snapshot、P09 input、I05 handoff 输出。
- paper_runtime_input_manifest_schema.yaml：定义 I04 输入清单。
- p08_permission_ingestion_schema.yaml：定义 P08 permission 接收与校验。
- runtime_permission_gate_schema.yaml：定义阻断无 P08 permission 或 P07 bypass 的门控。
- paper_candidate_queue_schema.yaml：定义纸面候选队列。
- paper_candidate_dedup_schema.yaml：定义重复候选去重。
- paper_position_uniqueness_schema.yaml：定义 one-token-one-position。
- paper_entry_price_model_schema.yaml：定义纸面入场价格模型。
- paper_slippage_application_schema.yaml：定义滑点应用。
- paper_cost_application_schema.yaml：定义费用应用。
- paper_position_open_schema.yaml：定义纸面开仓记录。
- paper_trade_schema.yaml：定义纸面交易记录。
- paper_position_update_schema.yaml：定义持仓更新。
- paper_mark_to_market_schema.yaml：定义按市场价格估值。
- runtime_invalidation_monitor_schema.yaml：定义运行中失效条件监控。
- paper_exit_rule_evaluation_schema.yaml：定义退出规则评估。
- paper_exit_event_schema.yaml：定义退出事件。
- paper_position_close_schema.yaml：定义仓位关闭记录。
- paper_equity_curve_schema.yaml：定义权益曲线。
- paper_runtime_risk_event_schema.yaml：定义运行风险事件。
- paper_runtime_snapshot_schema.yaml：定义 runtime 快照。
- paper_runtime_trace_schema.yaml：定义 runtime trace。
- paper_runtime_acceptance_result_schema.yaml：定义 runtime 验收结果。
- p09_review_replay_input_packet_contract.yaml：定义 P09 复盘输入包。
- i04_to_i05_handoff_contract.yaml：定义 I04_TO_I05 handoff packet。
- paper_runtime_policy.yaml：定义 paper-only runtime 总政策。
- paper_entry_policy.yaml：定义纸面入场政策。
- paper_update_policy.yaml：定义持仓更新政策。
- paper_exit_policy.yaml：定义退出政策。
- paper_cost_slippage_policy.yaml：定义滑点与费用政策。
- paper_risk_event_policy.yaml：定义风险事件政策。
- paper_runtime_hard_negative_rules.yaml：定义无 I03/P08 handoff、P07 bypass、真实下单、钱包签名、未登记路径、无 trace、无 P09 input 等阻断。
- paper_runtime_state_machine.yaml：定义 I04 全状态机。
- paper_runtime_trace_requirements.yaml：定义 paper runtime trace。
- i04_acceptance_criteria.md：定义 I04_READY / READY_WITH_GAPS / REJECTED / BLOCKED。
- i04_storage_constitution.md：定义系统文件和运行数据目录。
- i04_test_matrix.yaml：定义至少 20 个测试场景。
- i04_report_model.yaml：定义 I04 人类可读报告。
- i04_review_checklist.md：定义 I04 审计清单。
- her_i04_execution_protocol.md：定义 HER 执行 I04 的顺序和禁止事项。

运行输出要求：
1. paper_runtime_input_manifest.yaml
2. p08_permission_ingestion_records.yaml
3. runtime_permission_gate_records.yaml
4. paper_candidate_queue_records.yaml
5. paper_candidate_dedup_records.yaml
6. paper_position_uniqueness_records.yaml
7. paper_entry_price_model_records.yaml
8. paper_slippage_application_records.yaml
9. paper_cost_application_records.yaml
10. paper_position_open_records.yaml
11. paper_trade_records.yaml
12. paper_position_update_records.yaml
13. paper_mark_to_market_records.yaml
14. runtime_invalidation_monitor_records.yaml
15. paper_exit_rule_evaluation_records.yaml
16. paper_exit_event_records.yaml
17. paper_position_close_records.yaml
18. paper_equity_curve_records.yaml
19. paper_runtime_risk_event_records.yaml
20. paper_runtime_snapshot_records.yaml
21. p09_review_replay_input_packet.yaml
22. i04_paper_runtime_integration_report.md
23. i04_to_i05_handoff_packet.yaml
24. i04_acceptance_result.yaml

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. paper_runtime_input_manifest 摘要
4. P08 permission ingestion 摘要
5. runtime permission gate 摘要
6. candidate queue / dedup 摘要
7. position uniqueness 摘要
8. entry price model 摘要
9. slippage / cost application 摘要
10. paper position open 摘要
11. paper trade 摘要
12. position update / mark-to-market 摘要
13. invalidation monitor 摘要
14. exit rule evaluation 摘要
15. exit event / close record 摘要
16. equity curve 摘要
17. risk event 摘要
18. runtime snapshot 摘要
19. P09 review input packet 摘要
20. I04→I05 handoff 摘要
21. 是否允许进入 I05
22. 是否达到轻量机构级 I04 v1.0

最终验收标准：
只有当 I04 具备 paper runtime input manifest、P08 permission ingestion、runtime permission gate、candidate queue、candidate dedup、position uniqueness、entry price model、slippage application、cost application、paper position open、paper trade、position update、mark-to-market、invalidation monitor、exit rule evaluation、exit event、position close、equity curve、risk event、runtime snapshot、P09 review replay input packet、I04→I05 handoff、hard negative rules、state machine、trace requirements、acceptance criteria、storage constitution、test matrix、report model、HER execution protocol，并且没有 P07 bypass、没有 live execution、没有 wallet signing、没有 unregistered write、没有 missing trace、没有 missing P09 input 时，才允许标记为 I04_READY。
```

---

# 37. 当前是否达到专业化 I04 设计标准

## 判断

这一版 I04 达到：

```text
专业化
轻量机构水准
一次性把 I04 应有 runtime 对象补全
不是最小版本
不是普通纸面交易脚本
不是继续新增业务阶段
```

I04 被明确设计为：

```text
P08 permission 接收层
runtime permission gate 层
paper candidate queue 层
dedup / uniqueness 层
entry price / slippage / cost 层
paper position ledger 层
paper trade ledger 层
mark-to-market 层
invalidation monitor 层
exit rule / exit event 层
equity curve 层
risk event 层
runtime snapshot 层
P09 review replay input 层
I05 闭环回放前置层
```

---

# 38. I04 完成后下一步

I04 完成后进入：

```text
I05 Review / Upgrade Closed Loop
```

I05 才负责验证：

```text
P09 能否读取 I04 runtime 输出
P09 能否重建 P01-P08 决策链
P09 能否重建 Paper Runtime 运行路径
P09 能否生成 failure / success attribution
P10 能否读取 P09 升级候选
P10 能否生成 controlled upgrade package
P10 是否能生成 regression / rollback / implementation task packet
```

---

# 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|I04 是否已经有真实 paper runtime runner|当前定义了集成标准|实现阶段补齐 runner|
|滑点模型是否准确|I04 可应用默认或 P08 模型|P09/P10 校准|
|费用模型是否准确|I04 必须记录假设|P09/P10 校准|
|退出规则是否完整|I04 定义基础退出记录|后续通过 P09 样本校准|
|open / close / equity curve 是否与旧 paper_live 兼容|I04 不迁移旧数据|I05 可做 legacy replay 对照|
|Telegram 面板是否展示 paper runtime|I04 不负责面板|后续 Ops / Dashboard 层处理|
|是否进入实盘|不允许|当前仍是 paper-only 验证阶段|

---

# 本次认知升级点

1. **I04 的本质不是纸面交易脚本，而是 Paper-only Runtime Ledger。**
    
2. **P08 permission 是 I04 的唯一准入来源。**  
    P07 不能直接进入 Paper Runtime。
    
3. **纸面运行也必须有滑点、费用、风险事件、失效条件和 trace。**  
    否则 P09 无法判断系统能力是否真实。
    
4. **Paper Runtime 的核心产物不是收益率，而是可回放账本。**
    
5. **I04 必须同时记录 open、update、exit、close、equity、risk、snapshot。**
    
6. **I04 必须为 P09 生成 review replay input packet。**  
    没有这个包，纸面结果无法进入复盘归因闭环。
    
7. **I04 仍然不是实盘层。**  
    `PAPER_RUNTIME_ALLOWED` 永远不等于 `LIVE_EXECUTION_ALLOWED`。
    
8. **I04 完成后，系统才具备进入 I05 闭环回放验证的条件。**