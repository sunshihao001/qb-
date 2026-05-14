# P08 Execution Risk Controller 专业版 v3.0

## 执行前风控、报价安全、滑点费用、纸面运行许可与 Runtime 交接控制器

---

## 0. 先修正 P08 的定位

P08 不能被设计成：

```text
下单器
交易执行器
自动买入模块
纸面交易直接启动器
实盘风控模块
```

P08 的专业定位应该是：

```text
把 P07 交接过来的 PAPER_CANDIDATE / HUMAN_CONFIRMATION_REQUIRED 候选，经过报价一致性、安全扫描、流动性、滑点、费用、数据新鲜度、仓位限制、熔断规则、失效条件和 paper-only 约束检查后，裁决是否允许进入 Paper-only Runtime。
```

一句话定义：

> **P07 负责判断“是否值得交给执行前风控检查”。**  
> **P08 负责判断“当前是否允许进入纸面运行”。**  
> **Paper-only Runtime 才负责实际记录纸面入场、持仓更新、退出和统计。**

P08 可以输出：

```text
PAPER_RUNTIME_ALLOWED
PAPER_RUNTIME_BLOCKED
PAPER_RUNTIME_PAUSED
PAPER_RUNTIME_NEEDS_REFRESH
HUMAN_CONFIRMATION_REQUIRED
EXECUTION_RISK_REJECTED
```

P08 不能输出：

```text
LIVE_EXECUTION_ALLOWED
自动实盘买入
钱包签名
真实下单
真实成交确认
```

---

# 1. P08 阶段核心目标

P08 必须一次性解决 18 个问题：

|编号|核心问题|P08 必须输出|
|---|---|---|
|1|P07 的 PAPER_CANDIDATE 是否仍然有效？|`p07_candidate_validity_check_record`|
|2|当前报价是否可用、一致、未偏离？|`quote_consistency_record`|
|3|当前流动性是否足够纸面模拟？|`liquidity_depth_record`|
|4|滑点与价格冲击是否可接受？|`slippage_estimation_record`|
|5|手续费 / 成本模型是否可用？|`execution_cost_model_record`|
|6|安全风险是否需要阻断？|`security_recheck_record`|
|7|是否存在不可卖、黑名单、权限风险？|`sellability_risk_record`|
|8|数据是否足够新鲜？|`freshness_recheck_record`|
|9|P07 绑定的失效条件是否已触发？|`invalidation_precheck_record`|
|10|钱包 / 持仓 delta 是否需要刷新？|`wallet_delta_refresh_requirement_record`|
|11|是否触发全局风险限额？|`runtime_risk_limit_record`|
|12|是否违反 one-token-one-position？|`position_uniqueness_record`|
|13|是否触发连续失败 / 日亏损熔断？|`circuit_breaker_record`|
|14|是否允许进入纸面运行？|`paper_runtime_permission_record`|
|15|如果阻断，原因是什么？|`execution_risk_block_reason_record`|
|16|如果暂停，需要刷新什么？|`execution_risk_refresh_request_record`|
|17|Paper Runtime 应如何读取？|`paper_runtime_data_request_packet`|
|18|是否可交接给 Paper-only Runtime？|`p08_to_paper_runtime_handoff_packet`|

---

# 2. P08 的专业角色模型

|角色|负责问题|输出|
|---|---|---|
|报价审查官|当前价格是否可信|`quote_consistency_record`|
|流动性审查官|是否有足够可模拟深度|`liquidity_depth_record`|
|滑点成本官|纸面成交是否要考虑滑点和费用|`slippage_estimation_record` / `execution_cost_model_record`|
|安全审查官|是否存在合约、权限、不可卖风险|`security_recheck_record`|
|数据新鲜度官|P02/P07 的数据是否需要刷新|`freshness_recheck_record`|
|失效条件官|P07 绑定的 invalidation 是否触发|`invalidation_precheck_record`|
|风险限额官|日亏损、连续失败、仓位唯一性|`runtime_risk_limit_record`|
|Runtime 交接官|把允许样本交给纸面运行|`paper_runtime_permission_record` / `handoff_packet`|

---

# 3. P08 底层方法论

## 3.1 执行前风控不是策略判断

P08 不重新判断：

```text
这个币是不是好机会
是不是二段扩张
庄家是否还在
筹码是否未出完
```

这些已经由 P04-P07 处理。

P08 只判断：

```text
即使策略候选成立，当前是否具备可安全纸面模拟的执行条件。
```

---

## 3.2 PAPER_RUNTIME_ALLOWED 仍然不是实盘许可

P08 的最高权限是：

```text
允许进入 Paper-only Runtime
```

不是：

```text
允许真实交易
```

必须永久保留：

```text
live_execution_allowed: false
wallet_signing_allowed: false
auto_order_allowed: false
```

---

## 3.3 执行风险优先级高于策略吸引力

即使 P07 给出 PAPER_CANDIDATE，只要 P08 发现：

```text
报价异常
安全风险
滑点过大
流动性不足
数据过期
失效条件触发
连续失败熔断
日亏损限制触发
```

就必须输出：

```text
PAPER_RUNTIME_BLOCKED
或 PAPER_RUNTIME_PAUSED
```

---

## 3.4 P08 必须强制刷新关键执行数据

P07 的数据是策略门控上下文，不一定适合执行前判断。

P08 必须至少重新检查：

```text
当前报价
当前流动性
当前安全状态
当前 holder / wallet delta 需求
当前场景失效条件
当前风险限额
```

---

# 4. P08 支持的裁决状态

```yaml
p08_execution_risk_statuses:
  PAPER_RUNTIME_ALLOWED:
    meaning: 允许交给 Paper-only Runtime 记录纸面交易
    downstream: PAPER_ONLY_RUNTIME

  PAPER_RUNTIME_ALLOWED_WITH_LIMITATIONS:
    meaning: 允许纸面运行，但必须携带限制、滑点、费用和监控条件
    downstream: PAPER_ONLY_RUNTIME_LIMITED

  PAPER_RUNTIME_PAUSED:
    meaning: 暂停进入纸面运行，需要刷新或等待条件
    downstream: REFRESH_REQUIRED

  PAPER_RUNTIME_BLOCKED:
    meaning: 执行前风险阻断，不允许纸面运行
    downstream: STOP_RUNTIME

  HUMAN_CONFIRMATION_REQUIRED:
    meaning: 需要人工确认是否继续进入 P08 或纸面运行
    downstream: MANUAL_REVIEW

  EXECUTION_RISK_REJECTED:
    meaning: 不符合执行前风控标准
    downstream: STOP_DOWNSTREAM
```

---

# 5. P08 必须建立的核心对象

|对象|作用|
|---|---|
|`Execution Risk Input Manifest`|记录 P08 接收的 P07 候选与限制|
|`P07 Candidate Validity Check Record`|P07 候选是否仍有效|
|`Quote Snapshot Record`|当前报价快照|
|`Quote Consistency Record`|多源报价一致性|
|`Liquidity Depth Record`|流动性与深度|
|`Slippage Estimation Record`|滑点和价格冲击估算|
|`Execution Cost Model Record`|手续费、滑点、成本模型|
|`Security Recheck Record`|安全复查|
|`Sellability Risk Record`|是否可卖、转账限制、黑名单风险|
|`Freshness Recheck Record`|执行前新鲜度检查|
|`Invalidation Precheck Record`|P07 失效条件是否触发|
|`Wallet Delta Refresh Requirement Record`|是否需要钱包 delta 刷新|
|`Runtime Risk Limit Record`|全局风险限额|
|`Position Uniqueness Record`|单 token 持仓唯一性|
|`Circuit Breaker Record`|熔断规则|
|`Paper Entry Simulation Plan`|纸面入场模拟参数|
|`Paper Runtime Permission Record`|是否允许进入纸面运行|
|`Execution Risk Block Reason Record`|阻断原因|
|`Execution Risk Refresh Request Record`|刷新请求|
|`Paper Runtime Data Request Packet`|给纸面运行的数据请求|
|`P08 to Paper Runtime Handoff Packet`|P08 → Paper Runtime 交接包|

---

# 6. P08 输入：必须读取什么

```yaml
p08_required_inputs:
  from_p07:
    - p07_to_p08_handoff_packet
    - p08_execution_risk_data_request_packet
    - strategy_gate_decision_records
    - strategy_candidate_records
    - strategy_usage_permission_records
    - strategy_invalidation_binding_records
    - hard_negative_evaluation_records
    - strategy_gate_report

  from_p06:
    - scenario_risk_flag_records
    - scenario_invalidation_records
    - scenario_usage_permission_records

  from_p05:
    - counter_evidence_records
    - evidence_conflict_records
    - unknown_evidence_records

  from_p04:
    - chip_structure_quality_records
    - counterparty_pressure_records
    - chip_transfer_status_records
    - distribution_progress_records

  from_p02:
    - market_fact_records
    - security_fact_records
    - freshness_report
    - quote_or_market_fact_sources
    - data_quality_report

  from_runtime_state:
    - open_paper_positions
    - closed_paper_positions
    - risk_events
    - strategy_metrics
    - daily_paper_summary
    - circuit_breaker_state

  from_control_planes:
    - trace_handoff_packet
    - acceptance_result_packet
    - handoff_packet
    - downstream_read_instruction
    - limitation_transfer_packet
    - forbidden_use_policy
    - governance_handoff_packet
    - execution_risk_policy_handoff

  required_contracts:
    - p08_input_contract
    - p08_output_contract
    - execution_risk_decision_contract
    - paper_runtime_permission_contract
    - paper_runtime_input_contract
```

P08 启动前必须确认：

```text
P07 已验收
P07 handoff 已生成
候选状态为 PAPER_CANDIDATE 或 HUMAN_CONFIRMATION_REQUIRED
P08 不允许读取未授权字段
P08 不允许绕过 P07
P08 不允许直接实盘
P08 不允许钱包签名
```

---

# 7. Execution Risk Input Manifest

```yaml
execution_risk_input_manifest:
  manifest_id: string
  candidate_id: string
  token_address: string
  generated_at: datetime

  upstream_packets:
    p07_handoff_packet_id: string
    p08_data_request_packet_id: string
    trace_handoff_packet_id: string
    acceptance_result_packet_id: string

  p07_decision_context:
    strategy_gate_decision: string
    selected_strategy_profile: string | null
    strategy_candidate_id: string | null
    human_confirmation_required: boolean
    p08_allowed_by_p07: boolean

  inherited_limits:
    paper_only: true
    live_execution_allowed: false
    wallet_signing_allowed: false
    auto_order_allowed: false
    limitation_tags: list
    invalidation_ids: list

  input_quality:
    p07_decision_valid: boolean
    required_records_available: boolean
    missing_required_inputs: list
    input_quality_status:
      - EXECUTION_INPUT_HIGH_CONFIDENCE
      - EXECUTION_INPUT_USABLE
      - EXECUTION_INPUT_USABLE_WITH_GAPS
      - EXECUTION_INPUT_LOW_CONFIDENCE
      - EXECUTION_INPUT_UNUSABLE

  trace:
    execution_input_trace_id: string
    upstream_trace_ids: list
```

---

# 8. P07 Candidate Validity Check Record

```yaml
p07_candidate_validity_check_record:
  validity_check_id: string
  candidate_id: string

  checks:
    p07_decision_is_paper_candidate: boolean
    p07_usage_permission_send_to_p08: boolean
    no_later_block_event_detected: boolean
    invalidation_not_triggered_before_p08: boolean
    data_refresh_not_expired: boolean

  result:
    p07_candidate_still_valid: boolean
    validity_status:
      - VALID_FOR_P08
      - VALID_WITH_LIMITATIONS
      - NEEDS_REFRESH
      - INVALIDATED
      - BLOCKED

  invalidation_sources:
    triggered_invalidation_ids: list
    new_counter_risk_ids: list
    stale_input_ids: list

  downstream_effect:
    can_continue_execution_risk_check: boolean
    must_pause: boolean
    must_block: boolean
```

---

# 9. Quote Snapshot Record

```yaml
quote_snapshot_record:
  quote_snapshot_id: string
  candidate_id: string
  token_address: string
  collected_at: datetime

  quote_sources:
    - source_id: string
      price_usd: number | null
      market_cap_usd: number | null
      liquidity_usd: number | null
      bid_price_usd: number | null
      ask_price_usd: number | null
      spread_pct: number | null
      source_latency_ms: integer | null
      source_status:
        - SUCCESS
        - PARTIAL
        - EMPTY
        - FAILED
        - STALE

  selected_quote:
    selected_source_id: string | null
    selected_price_usd: number | null
    selected_market_cap_usd: number | null
    selected_liquidity_usd: number | null
    selection_reason: string

  freshness:
    quote_age_seconds: integer
    quote_freshness_status:
      - FRESH
      - ACCEPTABLE
      - STALE
      - EXPIRED
      - UNKNOWN

  trace:
    quote_trace_id: string
    source_pull_trace_ids: list
```

---

# 10. Quote Consistency Record

```yaml
quote_consistency_record:
  quote_consistency_id: string
  candidate_id: string

  quote_comparison:
    gmgn_price_usd: number | null
    okx_quote_price_usd: number | null
    chain_estimated_price_usd: number | null
    selected_price_usd: number | null

  deviation_metrics:
    max_source_deviation_pct: number | null
    gmgn_vs_okx_deviation_pct: number | null
    gmgn_vs_chain_deviation_pct: number | null
    okx_vs_chain_deviation_pct: number | null

  consistency_status:
    - QUOTE_CONSISTENT
    - QUOTE_MINOR_DEVIATION
    - QUOTE_MAJOR_DEVIATION
    - QUOTE_SOURCE_MISSING
    - QUOTE_UNUSABLE

  gate_effect:
    - SUPPORTS_RUNTIME
    - ALLOW_WITH_LIMITATION
    - REQUIRE_REFRESH
    - BLOCK_RUNTIME

  thresholds:
    minor_deviation_pct: number
    major_deviation_pct: number
    block_deviation_pct: number
```

---

# 11. Liquidity Depth Record

```yaml
liquidity_depth_record:
  liquidity_depth_id: string
  candidate_id: string

  liquidity_snapshot:
    liquidity_usd: number | null
    pool_address: string | null
    quote_token: string | null
    liquidity_age_seconds: integer | null

  depth_checks:
    minimum_liquidity_threshold_usd: number
    liquidity_above_minimum: boolean | null
    liquidity_change_5m_pct: number | null
    liquidity_drop_detected: boolean | null
    lp_removal_risk: string | null

  execution_capacity:
    simulated_entry_size_usd: number | null
    entry_size_to_liquidity_pct: number | null
    max_allowed_entry_size_usd: number | null
    liquidity_capacity_status:
      - SUFFICIENT
      - LIMITED
      - THIN
      - UNUSABLE
      - UNKNOWN

  gate_effect:
    - SUPPORTS_RUNTIME
    - LIMIT_POSITION_SIZE
    - REQUIRE_REFRESH
    - BLOCK_RUNTIME
```

---

# 12. Slippage Estimation Record

```yaml
slippage_estimation_record:
  slippage_id: string
  candidate_id: string

  simulated_order:
    side: PAPER_BUY
    simulated_entry_size_usd: number
    order_type_for_simulation:
      - MARKET_SIMULATION
      - LIMIT_SIMULATION
      - MID_PRICE_SIMULATION

  estimates:
    estimated_slippage_pct: number | null
    estimated_price_impact_pct: number | null
    estimated_effective_entry_price_usd: number | null
    worst_case_entry_price_usd: number | null

  thresholds:
    max_allowed_slippage_pct: number
    max_allowed_price_impact_pct: number

  slippage_status:
    - SLIPPAGE_ACCEPTABLE
    - SLIPPAGE_HIGH_LIMIT_SIZE
    - SLIPPAGE_TOO_HIGH
    - SLIPPAGE_UNKNOWN

  downstream:
    paper_runtime_must_use_effective_entry_price: boolean
    paper_runtime_must_record_slippage_model: boolean
```

---

# 13. Execution Cost Model Record

```yaml
execution_cost_model_record:
  cost_model_id: string
  candidate_id: string

  cost_components:
    estimated_network_fee_usd: number | null
    estimated_platform_fee_usd: number | null
    estimated_slippage_cost_usd: number | null
    estimated_spread_cost_usd: number | null
    total_estimated_cost_usd: number | null
    total_estimated_cost_pct: number | null

  cost_model_status:
    - COST_MODEL_READY
    - COST_MODEL_READY_WITH_GAPS
    - COST_MODEL_WEAK
    - COST_MODEL_UNUSABLE

  paper_runtime_requirement:
    apply_cost_model_to_paper_pnl: boolean
    record_cost_assumptions: boolean
    if_missing_cost_model:
      - BLOCK_RUNTIME
      - ALLOW_WITH_ZERO_COST_NOTE
      - ALLOW_WITH_DEFAULT_COST_MODEL
```

---

# 14. Security Recheck Record

```yaml
security_recheck_record:
  security_recheck_id: string
  candidate_id: string
  checked_at: datetime

  checks:
    mint_authority_status: string | null
    freeze_authority_status: string | null
    owner_permission_status: string | null
    blacklist_risk: string | null
    transfer_restriction_risk: string | null
    honeypot_risk: string | null
    tax_risk: string | null
    liquidity_lock_status: string | null
    lp_removal_risk: string | null

  security_status:
    - SECURITY_CLEAR_FOR_PAPER
    - SECURITY_CLEAR_WITH_LIMITATIONS
    - SECURITY_NEEDS_REFRESH
    - SECURITY_RISK_BLOCK
    - SECURITY_UNKNOWN_BLOCK

  hard_block_reasons:
    - MINT_AUTHORITY_ACTIVE
    - FREEZE_AUTHORITY_ACTIVE
    - BLACKLIST_RISK_DETECTED
    - TRANSFER_RESTRICTION_DETECTED
    - HONEYPOT_RISK_DETECTED
    - LP_REMOVAL_RISK_HIGH
    - SECURITY_DATA_STALE

  downstream_effect:
    paper_runtime_allowed: boolean
    p09_review_required_if_ignored: boolean
```

---

# 15. Sellability Risk Record

即使只是纸面，也必须记录“理论可卖性风险”，否则纸面结果会失真。

```yaml
sellability_risk_record:
  sellability_id: string
  candidate_id: string

  sellability_checks:
    can_sell_simulation_supported: boolean | null
    transfer_out_possible: boolean | null
    blacklist_or_restriction_absent: boolean | null
    pool_liquidity_available_for_exit: boolean | null
    exit_slippage_estimate_available: boolean | null

  sellability_status:
    - SELLABILITY_ACCEPTABLE
    - SELLABILITY_LIMITED
    - SELLABILITY_UNKNOWN
    - SELLABILITY_BLOCKED

  paper_runtime_effect:
    if_limited:
      - require_exit_slippage_model
      - require_risk_tag
      - reduce_position_size
    if_blocked:
      - block_paper_runtime
```

---

# 16. Freshness Recheck Record

```yaml
freshness_recheck_record:
  freshness_recheck_id: string
  candidate_id: string
  checked_at: datetime

  freshness_checks:
    quote_fresh: boolean
    liquidity_fresh: boolean
    security_fresh: boolean
    holder_snapshot_fresh: boolean | null
    wallet_delta_fresh: boolean | null
    scenario_context_fresh: boolean | null
    market_structure_fresh: boolean | null

  stale_inputs:
    - input_name: string
      source_controller: string
      age_seconds: integer | null
      required_refresh: boolean

  freshness_status:
    - FRESH_ENOUGH_FOR_PAPER_RUNTIME
    - FRESH_WITH_LIMITATIONS
    - REFRESH_REQUIRED
    - STALE_BLOCK_RUNTIME

  refresh_required:
    - QUOTE
    - LIQUIDITY
    - SECURITY
    - HOLDER_SNAPSHOT
    - WALLET_DELTA
    - SCENARIO_RERUN
    - EVIDENCE_RERUN
```

---

# 17. Invalidation Precheck Record

```yaml
invalidation_precheck_record:
  invalidation_precheck_id: string
  candidate_id: string

  inherited_invalidations:
    hard_invalidation_ids: list
    soft_invalidation_ids: list
    watch_invalidation_ids: list

  precheck_results:
    - invalidation_id: string
      condition_cn: string
      triggered: boolean | null
      trigger_source: string | null
      severity:
        - HARD_INVALIDATION
        - SOFT_INVALIDATION
        - WATCH_INVALIDATION

  invalidation_status:
    - NO_INVALIDATION_TRIGGERED
    - WATCH_INVALIDATION_TRIGGERED
    - SOFT_INVALIDATION_TRIGGERED
    - HARD_INVALIDATION_TRIGGERED
    - INVALIDATION_UNKNOWN_NEEDS_REFRESH

  gate_effect:
    - ALLOW_RUNTIME
    - ALLOW_WITH_MONITORING
    - PAUSE_RUNTIME
    - BLOCK_RUNTIME
```

---

# 18. Wallet Delta Refresh Requirement Record

P08 不一定自己做钱包分析，但要决定是否必须刷新。

```yaml
wallet_delta_refresh_requirement_record:
  wallet_delta_refresh_id: string
  candidate_id: string

  triggers:
    p07_requested_wallet_delta_refresh: boolean
    holder_snapshot_stale: boolean
    chip_structure_near_threshold: boolean
    high_counterparty_pressure_risk: boolean
    active_distribution_risk_recent: boolean

  refresh_decision:
    wallet_delta_refresh_required: boolean
    refresh_priority:
      - HIGH
      - MEDIUM
      - LOW
      - NONE

  required_refresh_outputs:
    - updated_holder_snapshot
    - updated_wallet_position_delta
    - updated_counterparty_pressure
    - updated_distribution_progress

  if_refresh_not_available:
    - PAUSE_RUNTIME
    - HUMAN_CONFIRMATION_REQUIRED
    - BLOCK_RUNTIME
```

---

# 19. Runtime Risk Limit Record

```yaml
runtime_risk_limit_record:
  risk_limit_id: string
  candidate_id: string

  global_limits:
    daily_max_loss_sol: number | null
    daily_max_failed_trades: integer | null
    max_open_paper_positions: integer | null
    max_candidates_per_cycle: integer | null
    max_position_size_usd: number | null

  current_runtime_state:
    current_daily_paper_loss_sol: number | null
    current_failed_trades_today: integer | null
    current_open_paper_positions: integer | null
    current_candidate_runtime_count: integer | null

  checks:
    daily_loss_limit_available: boolean
    daily_loss_limit_breached: boolean
    failed_trade_limit_breached: boolean
    max_open_positions_breached: boolean
    max_candidate_cycle_breached: boolean

  risk_limit_status:
    - RISK_LIMITS_CLEAR
    - RISK_LIMITS_WITH_WARNINGS
    - RISK_LIMITS_NEED_STATE_REFRESH
    - RISK_LIMITS_BLOCK_RUNTIME
```

---

# 20. Position Uniqueness Record

```yaml
position_uniqueness_record:
  uniqueness_id: string
  candidate_id: string
  token_address: string

  checks:
    existing_open_paper_position_same_token: boolean
    existing_recent_closed_position_same_token: boolean
    cooldown_active: boolean
    one_token_one_position_rule_enabled: boolean

  uniqueness_status:
    - UNIQUE_POSITION_ALLOWED
    - EXISTING_POSITION_BLOCKS
    - COOLDOWN_BLOCKS
    - NEEDS_POSITION_STATE_REFRESH

  downstream_effect:
    paper_runtime_allowed: boolean
    reason_cn: string
```

---

# 21. Circuit Breaker Record

```yaml
circuit_breaker_record:
  circuit_breaker_id: string
  checked_at: datetime

  breakers:
    consecutive_failures:
      enabled: true
      threshold: integer
      current_value: integer
      triggered: boolean

    daily_failed_trades:
      enabled: true
      threshold: integer
      current_value: integer
      triggered: boolean

    daily_loss:
      enabled: true
      threshold_sol: number | null
      current_loss_sol: number | null
      triggered: boolean

    data_failure_rate:
      enabled: true
      threshold_pct: number | null
      current_failure_rate_pct: number | null
      triggered: boolean

  circuit_status:
    - CIRCUIT_CLEAR
    - CIRCUIT_WARNING
    - CIRCUIT_TRIGGERED_PAUSE
    - CIRCUIT_TRIGGERED_BLOCK

  downstream_effect:
    paper_runtime_allowed: boolean
```

---

# 22. Paper Entry Simulation Plan

P08 可以设计纸面入场模拟计划，但不能直接写入持仓。

```yaml
paper_entry_simulation_plan:
  plan_id: string
  candidate_id: string
  strategy_candidate_id: string

  simulated_entry:
    entry_mode:
      - PAPER_MARKET_SIMULATION
      - PAPER_LIMIT_SIMULATION
      - PAPER_CONFIRMATION_REQUIRED
    reference_price_usd: number | null
    effective_entry_price_usd: number | null
    simulated_size_usd: number | null
    simulated_size_token: number | null

  cost_and_slippage:
    slippage_model_id: string
    cost_model_id: string
    apply_fees: boolean
    apply_slippage: boolean

  runtime_monitoring_requirements:
    monitor_invalidations: list
    monitor_exit_conditions: list
    monitor_security_refresh: boolean
    monitor_quote_freshness: boolean

  restrictions:
    paper_only: true
    no_live_order: true
    no_wallet_signing: true
```

---

# 23. Paper Runtime Permission Record

这是 P08 的核心输出。

```yaml
paper_runtime_permission_record:
  permission_id: string
  candidate_id: string
  token_address: string
  generated_at: datetime

  final_permission:
    - PAPER_RUNTIME_ALLOWED
    - PAPER_RUNTIME_ALLOWED_WITH_LIMITATIONS
    - PAPER_RUNTIME_PAUSED
    - PAPER_RUNTIME_BLOCKED
    - HUMAN_CONFIRMATION_REQUIRED
    - EXECUTION_RISK_REJECTED

  decision_basis:
    p07_candidate_validity_check_id: string
    quote_consistency_id: string
    liquidity_depth_id: string
    slippage_id: string
    cost_model_id: string
    security_recheck_id: string
    sellability_risk_id: string
    freshness_recheck_id: string
    invalidation_precheck_id: string
    runtime_risk_limit_id: string
    position_uniqueness_id: string
    circuit_breaker_id: string

  permission_reason_cn:
    primary_reason: string
    supporting_reasons: list
    blocking_reasons: list
    limitations: list

  paper_runtime_allowed: boolean
  live_execution_allowed: false
  wallet_signing_allowed: false

  if_allowed:
    paper_entry_simulation_plan_id: string | null
    paper_runtime_data_request_packet_id: string | null

  if_blocked:
    execution_risk_block_reason_id: string | null

  if_paused:
    execution_risk_refresh_request_id: string | null

  trace:
    permission_trace_id: string
    source_trace_ids: list
```

---

# 24. Execution Risk Block Reason Record

```yaml
execution_risk_block_reason_record:
  block_reason_id: string
  candidate_id: string

  block_type:
    - QUOTE_BLOCK
    - LIQUIDITY_BLOCK
    - SLIPPAGE_BLOCK
    - SECURITY_BLOCK
    - SELLABILITY_BLOCK
    - FRESHNESS_BLOCK
    - INVALIDATION_BLOCK
    - RISK_LIMIT_BLOCK
    - POSITION_UNIQUENESS_BLOCK
    - CIRCUIT_BREAKER_BLOCK
    - GOVERNANCE_BLOCK
    - LIVE_EXECUTION_BLOCK

  block_reasons:
    - reason_id: string
      reason_cn: string
      source_record_id: string
      severity:
        - HARD
        - HIGH
        - MEDIUM

  recheck_allowed: boolean
  required_recheck_sources: list

  downstream:
    paper_runtime_handoff_allowed: false
    p09_review_required: boolean
```

---

# 25. Execution Risk Refresh Request Record

```yaml
execution_risk_refresh_request_record:
  refresh_request_id: string
  candidate_id: string

  refresh_reason:
    - QUOTE_STALE
    - LIQUIDITY_STALE
    - SECURITY_STALE
    - HOLDER_SNAPSHOT_STALE
    - WALLET_DELTA_REQUIRED
    - SCENARIO_INVALIDATION_UNKNOWN
    - POSITION_STATE_STALE
    - RISK_LIMIT_STATE_STALE

  required_refresh_tasks:
    - task_id: string
      target_controller:
        - P02_SOURCE_DATA_FACT_CONTROLLER
        - P03_WALLET_ENTITY_CONTROLLER
        - P04_CHIP_STRUCTURE_CONTROLLER
        - P05_EVIDENCE_CONTROLLER
        - P06_SCENARIO_RECOGNITION_CONTROLLER
        - P07_STRATEGY_GATE_CONTROLLER
      required_output: string
      priority:
        - HIGH
        - MEDIUM
        - LOW

  after_refresh_action:
    - RERUN_P08
    - RERUN_P07_THEN_P08
    - KEEP_PAUSED
    - BLOCK_IF_EXPIRED
```

---

# 26. Paper Runtime Data Request Packet

```yaml
paper_runtime_data_request_packet:
  packet_id: string
  from_controller: P08_EXECUTION_RISK_CONTROLLER
  to_runtime: PAPER_ONLY_RUNTIME
  generated_at: datetime

  candidate_scope:
    candidate_ids: list
    token_addresses: list
    chain: string

  allowed_runtime_inputs:
    paper_runtime_permission_records_path: string
    paper_entry_simulation_plans_path: string
    strategy_candidate_records_path: string
    strategy_gate_decision_records_path: string
    quote_snapshot_records_path: string
    slippage_estimation_records_path: string
    execution_cost_model_records_path: string
    invalidation_precheck_records_path: string

  required_runtime_actions:
    - create_or_update_paper_position
    - use_effective_entry_price
    - apply_slippage_model
    - apply_cost_model
    - record_invalidation_bindings
    - write_runtime_trace
    - write_risk_event_if_limited

  forbidden_runtime_actions:
    - live_order
    - wallet_signing
    - auto_swap
    - bypass_risk_limit
    - ignore_slippage_model
    - ignore_cost_model
    - ignore_invalidation_conditions

  runtime_limits:
    paper_only: true
    live_execution_allowed: false
    max_position_size_usd: number | null
    one_token_one_position_rule: boolean
```

---

# 27. P08 to Paper Runtime Handoff Packet

```yaml
p08_to_paper_runtime_handoff_packet:
  packet_id: string
  packet_type: P08_TO_PAPER_RUNTIME_HANDOFF
  generated_at: datetime

  route:
    from_controller: P08_EXECUTION_RISK_CONTROLLER
    to_runtime: PAPER_ONLY_RUNTIME

  upstream_control:
    p07_handoff_packet_id: string
    p08_acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    handoff_trace_id: string

  candidate_scope:
    candidate_count_total: integer
    paper_runtime_allowed_count: integer
    allowed_with_limitations_count: integer
    paused_count: integer
    blocked_count: integer
    human_confirmation_required_count: integer
    rejected_count: integer

  execution_risk_package:
    input_manifest_path: string
    p07_candidate_validity_check_records_path: string
    quote_snapshot_records_path: string
    quote_consistency_records_path: string
    liquidity_depth_records_path: string
    slippage_estimation_records_path: string
    execution_cost_model_records_path: string
    security_recheck_records_path: string
    sellability_risk_records_path: string
    freshness_recheck_records_path: string
    invalidation_precheck_records_path: string
    wallet_delta_refresh_requirement_records_path: string
    runtime_risk_limit_records_path: string
    position_uniqueness_records_path: string
    circuit_breaker_records_path: string
    paper_entry_simulation_plans_path: string
    paper_runtime_permission_records_path: string
    block_reason_records_path: string
    refresh_request_records_path: string

  paper_runtime_request:
    paper_runtime_data_request_packet_path: string
    candidates_allowed_for_runtime: list
    candidates_blocked_from_runtime: list

  quality:
    p08_execution_risk_report_path: string
    quote_quality_summary: object
    liquidity_quality_summary: object
    security_quality_summary: object
    risk_limit_summary: object

  limitations:
    - PAPER_ONLY_RUNTIME_PERMISSION
    - PAPER_RUNTIME_ALLOWED_IS_NOT_LIVE_PERMISSION
    - NO_WALLET_SIGNING
    - NO_LIVE_ORDER
    - LIVE_EXECUTION_FORBIDDEN

  downstream_permission:
    allowed:
      - PAPER_ONLY_RUNTIME
    forbidden:
      - LIVE_EXECUTION
      - WALLET_SIGNING
      - AUTO_ORDER_ROUTER

  read_instruction:
    paper_runtime_must_read_first:
      - p08_to_paper_runtime_handoff_packet
      - paper_runtime_data_request_packet
      - paper_runtime_permission_records
      - paper_entry_simulation_plans
      - quote_snapshot_records
      - slippage_estimation_records
      - execution_cost_model_records
      - invalidation_precheck_records
```

---

# 28. P08 Gap Policy

```yaml
p08_gap_policy:
  BLOCKING_GAP:
    result: P08_BLOCKED
    examples:
      - p07_handoff_missing
      - trace_missing
      - acceptance_missing
      - live_execution_requested
      - wallet_signing_requested
      - handoff_plane_bypassed

  CRITICAL_GAP:
    result: P08_REJECTED
    examples:
      - no_paper_candidate_from_p07
      - quote_unavailable
      - liquidity_unavailable
      - security_recheck_unavailable
      - no_runtime_permission_contract
      - output_contract_missing

  HIGH_GAP:
    result: P08_PAUSED_OR_BLOCKED
    examples:
      - quote_major_deviation
      - liquidity_thin
      - slippage_too_high
      - security_risk_detected
      - hard_invalidation_triggered
      - circuit_breaker_triggered

  MEDIUM_GAP:
    result: P08_ALLOWED_WITH_LIMITATIONS_OR_PAUSED
    examples:
      - holder_snapshot_stale
      - wallet_delta_refresh_required
      - execution_cost_model_weak
      - soft_invalidation_triggered
      - risk_limit_state_stale

  LOW_GAP:
    result: P08_ALLOWED_WITH_NOTE
    examples:
      - minor_quote_deviation
      - noncritical_cost_field_missing
      - optional_runtime_metadata_missing
```

---

# 29. P08 Hard Negative Rules

```yaml
p08_hard_negative_rules:
  - rule_id: P08_BLOCK_001
    name: 未读取 P07 handoff
    condition: p07_to_p08_handoff_packet_missing == true
    result: P08_BLOCKED
    reason: P08 不能绕过 P07 / Handoff 启动

  - rule_id: P08_BLOCK_002
    name: 无 P07 纸面候选
    condition: no_candidate_with_p07_decision_in [PAPER_CANDIDATE, HUMAN_CONFIRMATION_REQUIRED]
    result: P08_REJECTED
    reason: 没有可执行前风控检查的候选

  - rule_id: P08_BLOCK_003
    name: 报价不可用
    condition: quote_snapshot_missing == true or quote_status == QUOTE_UNUSABLE
    result: P08_BLOCKED
    reason: 无报价不能进入纸面运行

  - rule_id: P08_BLOCK_004
    name: 多源报价严重冲突
    condition: quote_consistency_status == QUOTE_MAJOR_DEVIATION
    result: P08_BLOCKED
    reason: 报价冲突会污染纸面入场价

  - rule_id: P08_BLOCK_005
    name: 流动性不足
    condition: liquidity_capacity_status in [THIN, UNUSABLE]
    result: P08_BLOCKED
    reason: 流动性不足，纸面模拟失真

  - rule_id: P08_BLOCK_006
    name: 滑点过高
    condition: slippage_status == SLIPPAGE_TOO_HIGH
    result: P08_BLOCKED
    reason: 滑点不可接受

  - rule_id: P08_BLOCK_007
    name: 安全风险阻断
    condition: security_status in [SECURITY_RISK_BLOCK, SECURITY_UNKNOWN_BLOCK]
    result: P08_BLOCKED
    reason: 安全风险未通过执行前检查

  - rule_id: P08_BLOCK_008
    name: 场景硬失效已触发
    condition: invalidation_status == HARD_INVALIDATION_TRIGGERED
    result: P08_BLOCKED
    reason: P07 绑定失效条件已触发

  - rule_id: P08_BLOCK_009
    name: 风险熔断触发
    condition: circuit_status in [CIRCUIT_TRIGGERED_PAUSE, CIRCUIT_TRIGGERED_BLOCK]
    result: P08_BLOCKED
    reason: 当前运行风险状态不允许新增纸面样本

  - rule_id: P08_BLOCK_010
    name: 重复持仓
    condition: uniqueness_status in [EXISTING_POSITION_BLOCKS, COOLDOWN_BLOCKS]
    result: P08_BLOCKED
    reason: 单 token 仓位唯一性或冷却期阻断

  - rule_id: P08_BLOCK_011
    name: 直接实盘或钱包签名请求
    condition: live_execution_requested == true or wallet_signing_requested == true
    result: P08_BLOCKED
    reason: 当前系统禁止自动实盘与钱包签名
```

---

# 30. P08 状态机专业版

```yaml
p08_execution_risk_state_machine:
  states:
    - P08_UNINITIALIZED
    - P08_CONTEXT_LOADED
    - P08_HANDOFF_READ
    - P08_INPUT_MANIFEST_BUILT
    - P08_P07_CANDIDATE_VALIDITY_CHECKED
    - P08_QUOTE_SNAPSHOT_COLLECTED
    - P08_QUOTE_CONSISTENCY_CHECKED
    - P08_LIQUIDITY_DEPTH_CHECKED
    - P08_SLIPPAGE_ESTIMATED
    - P08_COST_MODEL_BUILT
    - P08_SECURITY_RECHECKED
    - P08_SELLABILITY_CHECKED
    - P08_FRESHNESS_RECHECKED
    - P08_INVALIDATION_PRECHECKED
    - P08_WALLET_DELTA_REFRESH_EVALUATED
    - P08_RUNTIME_RISK_LIMIT_CHECKED
    - P08_POSITION_UNIQUENESS_CHECKED
    - P08_CIRCUIT_BREAKER_CHECKED
    - P08_PAPER_ENTRY_SIMULATION_PLAN_BUILT
    - P08_PERMISSION_DECISIONS_BUILT
    - P08_BLOCK_REASONS_BUILT
    - P08_REFRESH_REQUESTS_BUILT
    - P08_GAP_ANALYZED
    - P08_PAPER_RUNTIME_DATA_REQUEST_BUILT
    - P08_READY_FOR_ACCEPTANCE
    - P08_ACCEPTANCE_READY
    - P08_READY_FOR_PAPER_RUNTIME_HANDOFF
    - P08_READY_WITH_GAPS
    - P08_REJECTED
    - P08_BLOCKED

  critical_transitions:
    - from: P08_HANDOFF_READ
      to: P08_INPUT_MANIFEST_BUILT
      condition: p07_handoff_valid == true

    - from: P08_INPUT_MANIFEST_BUILT
      to: P08_P07_CANDIDATE_VALIDITY_CHECKED
      condition: p07_candidate_validity_records_created == true

    - from: P08_P07_CANDIDATE_VALIDITY_CHECKED
      to: P08_QUOTE_SNAPSHOT_COLLECTED
      condition: candidate_not_invalidated == true

    - from: P08_QUOTE_SNAPSHOT_COLLECTED
      to: P08_QUOTE_CONSISTENCY_CHECKED
      condition: quote_snapshot_records_created == true

    - from: P08_QUOTE_CONSISTENCY_CHECKED
      to: P08_LIQUIDITY_DEPTH_CHECKED
      condition: quote_consistency_records_created == true

    - from: P08_LIQUIDITY_DEPTH_CHECKED
      to: P08_SLIPPAGE_ESTIMATED
      condition: liquidity_depth_records_created == true

    - from: P08_SLIPPAGE_ESTIMATED
      to: P08_COST_MODEL_BUILT
      condition: slippage_estimation_records_created == true

    - from: P08_COST_MODEL_BUILT
      to: P08_SECURITY_RECHECKED
      condition: execution_cost_model_records_created == true

    - from: P08_SECURITY_RECHECKED
      to: P08_FRESHNESS_RECHECKED
      condition: security_recheck_records_created == true

    - from: P08_FRESHNESS_RECHECKED
      to: P08_INVALIDATION_PRECHECKED
      condition: freshness_recheck_records_created == true

    - from: P08_INVALIDATION_PRECHECKED
      to: P08_RUNTIME_RISK_LIMIT_CHECKED
      condition: invalidation_precheck_records_created == true

    - from: P08_RUNTIME_RISK_LIMIT_CHECKED
      to: P08_POSITION_UNIQUENESS_CHECKED
      condition: runtime_risk_limit_records_created == true

    - from: P08_POSITION_UNIQUENESS_CHECKED
      to: P08_CIRCUIT_BREAKER_CHECKED
      condition: position_uniqueness_records_created == true

    - from: P08_CIRCUIT_BREAKER_CHECKED
      to: P08_PERMISSION_DECISIONS_BUILT
      condition: circuit_breaker_records_created == true

    - from: P08_PERMISSION_DECISIONS_BUILT
      to: P08_PAPER_RUNTIME_DATA_REQUEST_BUILT
      condition: paper_runtime_permission_records_created == true

    - from: P08_PAPER_RUNTIME_DATA_REQUEST_BUILT
      to: P08_READY_FOR_ACCEPTANCE
      condition: p08_output_contract_ready == true

    - from: P08_READY_FOR_ACCEPTANCE
      to: P08_ACCEPTANCE_READY
      condition: acceptance_status in [ACCEPTANCE_READY, ACCEPTANCE_READY_WITH_GAPS]

    - from: P08_ACCEPTANCE_READY
      to: P08_READY_FOR_PAPER_RUNTIME_HANDOFF
      condition: p08_to_paper_runtime_handoff_packet_created == true
```

---

# 31. P08 文件体系

## 31.1 系统目录

```text
/root/sikk-gmgn/system/phase_controllers/p08_execution_risk_controller/
```

必须创建：

```text
p08_execution_risk_controller.yaml
p08_execution_risk_context.md
p08_input_contract.yaml
p08_output_contract.yaml
execution_risk_input_manifest_schema.yaml
p07_candidate_validity_check_schema.yaml
quote_snapshot_schema.yaml
quote_consistency_schema.yaml
liquidity_depth_schema.yaml
slippage_estimation_schema.yaml
execution_cost_model_schema.yaml
security_recheck_schema.yaml
sellability_risk_schema.yaml
freshness_recheck_schema.yaml
invalidation_precheck_schema.yaml
wallet_delta_refresh_requirement_schema.yaml
runtime_risk_limit_schema.yaml
position_uniqueness_schema.yaml
circuit_breaker_schema.yaml
paper_entry_simulation_plan_schema.yaml
paper_runtime_permission_schema.yaml
execution_risk_block_reason_schema.yaml
execution_risk_refresh_request_schema.yaml
paper_runtime_data_request_packet_contract.yaml
p08_to_paper_runtime_handoff_contract.yaml
execution_risk_policy.yaml
quote_consistency_policy.yaml
liquidity_depth_policy.yaml
slippage_policy.yaml
execution_cost_policy.yaml
security_recheck_policy.yaml
freshness_recheck_policy.yaml
runtime_risk_limit_policy.yaml
circuit_breaker_policy.yaml
paper_runtime_permission_policy.yaml
execution_risk_gap_policy.yaml
execution_risk_hard_negative_rules.yaml
execution_risk_state_machine.yaml
execution_risk_trace_requirements.yaml
p08_acceptance_criteria.md
p08_storage_constitution.md
p08_test_matrix.yaml
p08_report_model.yaml
p08_review_checklist.md
her_p08_execution_protocol.md
```

---

## 31.2 运行数据目录

```text
/root/sikk-gmgn/data/phase_controllers/p08_execution_risk/
  input_manifest/
  candidate_validity/
  quote_snapshots/
  quote_consistency/
  liquidity_depth/
  slippage/
  cost_model/
  security_recheck/
  sellability/
  freshness/
  invalidation_precheck/
  wallet_delta_refresh/
  runtime_risk_limits/
  position_uniqueness/
  circuit_breakers/
  paper_entry_simulation/
  paper_runtime_permissions/
  block_reasons/
  refresh_requests/
  paper_runtime_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/
```

---

# 32. P08 测试矩阵

```yaml
p08_test_matrix:
  - test_id: P08_TEST_001
    name: P07 PAPER_CANDIDATE，报价一致，安全通过，流动性充足
    expected_permission: PAPER_RUNTIME_ALLOWED

  - test_id: P08_TEST_002
    name: 缺 P07 handoff
    expected_status: P08_BLOCKED

  - test_id: P08_TEST_003
    name: P07 未给 PAPER_CANDIDATE
    expected_status: P08_REJECTED

  - test_id: P08_TEST_004
    name: 报价缺失
    expected_status: P08_BLOCKED

  - test_id: P08_TEST_005
    name: GMGN 与 OKX 报价严重偏离
    expected_status: P08_BLOCKED

  - test_id: P08_TEST_006
    name: 流动性不足
    expected_status: P08_BLOCKED

  - test_id: P08_TEST_007
    name: 滑点过高
    expected_status: P08_BLOCKED

  - test_id: P08_TEST_008
    name: 安全扫描发现 freeze 或 blacklist 风险
    expected_status: P08_BLOCKED

  - test_id: P08_TEST_009
    name: security scan 过期
    expected_status: P08_PAUSED_OR_REFRESH_REQUIRED

  - test_id: P08_TEST_010
    name: P07 hard invalidation 已触发
    expected_status: P08_BLOCKED

  - test_id: P08_TEST_011
    name: holder snapshot stale 但其他执行条件合格
    expected_status: P08_ALLOWED_WITH_LIMITATIONS_OR_PAUSED

  - test_id: P08_TEST_012
    name: 已存在同 token 开放纸面仓位
    expected_status: P08_BLOCKED

  - test_id: P08_TEST_013
    name: 连续失败熔断触发
    expected_status: P08_BLOCKED

  - test_id: P08_TEST_014
    name: 成本模型缺失但 policy 允许默认模型
    expected_status: PAPER_RUNTIME_ALLOWED_WITH_LIMITATIONS

  - test_id: P08_TEST_015
    name: P08 输出 live execution allowed
    expected_status: P08_BLOCKED

  - test_id: P08_TEST_016
    name: 钱包签名请求
    expected_status: P08_BLOCKED

  - test_id: P08_TEST_017
    name: PAPER_RUNTIME_ALLOWED 但未生成 paper_runtime_data_request
    expected_status: P08_BLOCKED

  - test_id: P08_TEST_018
    name: quote fresh 但 liquidity stale
    expected_status: P08_PAUSED_OR_REFRESH_REQUIRED
```

---

# 33. P08 报告模型

```yaml
p08_execution_risk_report:
  report_id: string
  generated_at: datetime
  controller_id: P08_EXECUTION_RISK_CONTROLLER

  summary:
    candidate_count_received: integer
    candidate_count_processed: integer
    paper_runtime_allowed_count: integer
    allowed_with_limitations_count: integer
    paused_count: integer
    blocked_count: integer
    human_confirmation_required_count: integer
    rejected_count: integer

  permission_distribution:
    PAPER_RUNTIME_ALLOWED: integer
    PAPER_RUNTIME_ALLOWED_WITH_LIMITATIONS: integer
    PAPER_RUNTIME_PAUSED: integer
    PAPER_RUNTIME_BLOCKED: integer
    HUMAN_CONFIRMATION_REQUIRED: integer
    EXECUTION_RISK_REJECTED: integer

  quote_summary:
    quote_consistent_count: integer
    quote_minor_deviation_count: integer
    quote_major_deviation_count: integer
    quote_unusable_count: integer

  liquidity_summary:
    sufficient_count: integer
    limited_count: integer
    thin_count: integer
    unusable_count: integer

  security_summary:
    security_clear_count: integer
    security_limited_count: integer
    security_block_count: integer
    security_unknown_count: integer

  risk_limit_summary:
    risk_clear_count: integer
    circuit_warning_count: integer
    circuit_triggered_count: integer
    duplicate_position_block_count: integer

  block_reason_summary:
    quote_blocks: integer
    liquidity_blocks: integer
    slippage_blocks: integer
    security_blocks: integer
    invalidation_blocks: integer
    circuit_breaker_blocks: integer
    duplicate_position_blocks: integer

  paper_runtime_handoff_summary:
    handoff_ready: boolean
    candidates_allowed_for_runtime: integer
    candidates_blocked_from_runtime: integer
    runtime_request_packet_path: string

  compliance:
    live_execution_allowed_generated: false
    wallet_signing_allowed_generated: false
    auto_order_generated: false
    paper_runtime_bypassed: false
```

---

# 34. HER P08 执行协议

```text
HER 执行 P08 时必须按以下顺序：

1. 读取 professional_build_order.md
2. 读取 phase_controller_index.yaml
3. 读取 P08 controller context
4. 读取 P07 → P08 handoff packet
5. 读取 p08_execution_risk_data_request_packet
6. 读取 Trace / Acceptance / Handoff 输出
7. 建立 execution_risk_input_manifest
8. 校验 P07 candidate validity
9. 拉取或读取当前 quote snapshot
10. 执行 quote consistency check
11. 执行 liquidity depth check
12. 执行 slippage estimation
13. 建立 execution cost model
14. 执行 security recheck
15. 执行 sellability risk check
16. 执行 freshness recheck
17. 执行 invalidation precheck
18. 判断 wallet delta refresh requirement
19. 检查 runtime risk limits
20. 检查 position uniqueness
21. 检查 circuit breaker
22. 建立 paper entry simulation plan
23. 生成 paper_runtime_permission_record
24. 生成 execution_risk_block_reason_record
25. 生成 execution_risk_refresh_request_record
26. 生成 P08 gap report
27. 生成 paper_runtime_data_request_packet
28. 写入 P08 trace
29. 生成 p08_execution_risk_report
30. 生成 p08_to_paper_runtime_handoff_packet
31. 执行 P08 acceptance
32. 只允许 handoff 给 Paper-only Runtime
```

禁止：

```text
1. 不允许无 P07 handoff 启动 P08
2. 不允许无 PAPER_CANDIDATE 做执行前风控
3. 不允许无 quote 进入纸面运行
4. 不允许忽略报价冲突
5. 不允许忽略滑点和成本模型
6. 不允许忽略安全复查
7. 不允许忽略 P07 绑定的 invalidation
8. 不允许忽略 runtime risk limits
9. 不允许重复 token 纸面开仓
10. 不允许绕过 Paper Runtime Handoff
11. 不允许生成 live execution permission
12. 不允许钱包签名
13. 不允许真实下单
```

---

# 35. 给 HER 的专业化任务书

```text
任务名称：建立 P08 Execution Risk Controller 专业版 v3.0

目标：
在 /root/sikk-gmgn/system/phase_controllers/p08_execution_risk_controller/ 下建立 P08 Execution Risk Controller。该控制器不是下单器，不是实盘执行器，也不是纸面交易运行器，而是执行前风控、报价安全、滑点费用、纸面运行许可与 Paper-only Runtime 交接控制器。它负责读取 P07 Strategy Gate Controller 输出的 PAPER_CANDIDATE、strategy gate decision、invalidation bindings 和 p08_execution_risk_data_request_packet，重新检查当前报价、一致性、流动性、滑点、费用、安全、可卖性、数据新鲜度、失效条件、风险限额、持仓唯一性和熔断状态，最终输出 PAPER_RUNTIME_ALLOWED / PAPER_RUNTIME_ALLOWED_WITH_LIMITATIONS / PAPER_RUNTIME_PAUSED / PAPER_RUNTIME_BLOCKED / HUMAN_CONFIRMATION_REQUIRED，并生成 Paper Runtime Data Request Packet 与 P08→Paper Runtime Handoff Packet。

核心原则：
1. P08 只做执行前风控与纸面运行许可。
2. P08 不执行交易。
3. P08 不做钱包签名。
4. P08 不允许 live execution。
5. P08 不允许绕过 P07。
6. P08 不允许绕过 Paper-only Runtime。
7. P08 必须重新检查当前 quote。
8. P08 必须检查 quote consistency。
9. P08 必须检查 liquidity depth。
10. P08 必须估算 slippage。
11. P08 必须建立 execution cost model。
12. P08 必须执行 security recheck。
13. P08 必须检查 sellability risk。
14. P08 必须检查 freshness。
15. P08 必须检查 P07 绑定的 invalidation conditions。
16. P08 必须检查 runtime risk limits、position uniqueness 和 circuit breaker。
17. P08 必须生成 Paper Runtime Data Request Packet。
18. P08 只能交接给 Paper-only Runtime。

需要创建系统目录：
/root/sikk-gmgn/system/phase_controllers/p08_execution_risk_controller/

需要创建系统文件：
1. p08_execution_risk_controller.yaml
2. p08_execution_risk_context.md
3. p08_input_contract.yaml
4. p08_output_contract.yaml
5. execution_risk_input_manifest_schema.yaml
6. p07_candidate_validity_check_schema.yaml
7. quote_snapshot_schema.yaml
8. quote_consistency_schema.yaml
9. liquidity_depth_schema.yaml
10. slippage_estimation_schema.yaml
11. execution_cost_model_schema.yaml
12. security_recheck_schema.yaml
13. sellability_risk_schema.yaml
14. freshness_recheck_schema.yaml
15. invalidation_precheck_schema.yaml
16. wallet_delta_refresh_requirement_schema.yaml
17. runtime_risk_limit_schema.yaml
18. position_uniqueness_schema.yaml
19. circuit_breaker_schema.yaml
20. paper_entry_simulation_plan_schema.yaml
21. paper_runtime_permission_schema.yaml
22. execution_risk_block_reason_schema.yaml
23. execution_risk_refresh_request_schema.yaml
24. paper_runtime_data_request_packet_contract.yaml
25. p08_to_paper_runtime_handoff_contract.yaml
26. execution_risk_policy.yaml
27. quote_consistency_policy.yaml
28. liquidity_depth_policy.yaml
29. slippage_policy.yaml
30. execution_cost_policy.yaml
31. security_recheck_policy.yaml
32. freshness_recheck_policy.yaml
33. runtime_risk_limit_policy.yaml
34. circuit_breaker_policy.yaml
35. paper_runtime_permission_policy.yaml
36. execution_risk_gap_policy.yaml
37. execution_risk_hard_negative_rules.yaml
38. execution_risk_state_machine.yaml
39. execution_risk_trace_requirements.yaml
40. p08_acceptance_criteria.md
41. p08_storage_constitution.md
42. p08_test_matrix.yaml
43. p08_report_model.yaml
44. p08_review_checklist.md
45. her_p08_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/phase_controllers/p08_execution_risk/
  input_manifest/
  candidate_validity/
  quote_snapshots/
  quote_consistency/
  liquidity_depth/
  slippage/
  cost_model/
  security_recheck/
  sellability/
  freshness/
  invalidation_precheck/
  wallet_delta_refresh/
  runtime_risk_limits/
  position_uniqueness/
  circuit_breakers/
  paper_entry_simulation/
  paper_runtime_permissions/
  block_reasons/
  refresh_requests/
  paper_runtime_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/

每个文件要求：
- p08_execution_risk_controller.yaml：定义 P08 身份、职责、权限、上下游、状态码、禁止事项。
- p08_execution_risk_context.md：写成 HER 执行前必须读取的 P08 上下文。
- p08_input_contract.yaml：定义 P08 必须读取的 P07 handoff、strategy candidate、decision、usage permission、invalidation bindings、runtime state。
- p08_output_contract.yaml：定义 quote、security、slippage、risk limit、paper permission、handoff 输出。
- execution_risk_input_manifest_schema.yaml：定义 P08 接收的所有执行前风控输入。
- p07_candidate_validity_check_schema.yaml：定义 P07 候选有效性检查。
- quote_snapshot_schema.yaml：定义当前报价快照。
- quote_consistency_schema.yaml：定义多源报价一致性。
- liquidity_depth_schema.yaml：定义流动性深度与容量。
- slippage_estimation_schema.yaml：定义滑点和价格冲击估算。
- execution_cost_model_schema.yaml：定义费用、滑点、价差和总成本模型。
- security_recheck_schema.yaml：定义安全复查。
- sellability_risk_schema.yaml：定义理论可卖性风险。
- freshness_recheck_schema.yaml：定义执行前新鲜度复查。
- invalidation_precheck_schema.yaml：定义 P07 绑定失效条件复查。
- wallet_delta_refresh_requirement_schema.yaml：定义是否需要钱包 delta / holder snapshot 刷新。
- runtime_risk_limit_schema.yaml：定义日亏损、失败次数、开放仓位、候选数量限制。
- position_uniqueness_schema.yaml：定义单 token 单纸面持仓和冷却期规则。
- circuit_breaker_schema.yaml：定义连续失败、日失败、日亏损、数据失败率熔断。
- paper_entry_simulation_plan_schema.yaml：定义纸面入场模拟参数。
- paper_runtime_permission_schema.yaml：定义 PAPER_RUNTIME_ALLOWED / BLOCKED / PAUSED 等裁决。
- execution_risk_block_reason_schema.yaml：定义执行风险阻断原因。
- execution_risk_refresh_request_schema.yaml：定义需要刷新哪些上游数据。
- paper_runtime_data_request_packet_contract.yaml：定义 P08 给 Paper-only Runtime 的数据请求包。
- p08_to_paper_runtime_handoff_contract.yaml：定义 P08_TO_PAPER_RUNTIME handoff packet。
- execution_risk_policy.yaml：定义 P08 总体执行前风控政策。
- quote_consistency_policy.yaml：定义报价偏差阈值和处理规则。
- liquidity_depth_policy.yaml：定义最小流动性和仓位容量。
- slippage_policy.yaml：定义最大滑点和价格冲击。
- execution_cost_policy.yaml：定义费用模型。
- security_recheck_policy.yaml：定义安全阻断条件。
- freshness_recheck_policy.yaml：定义执行前新鲜度要求。
- runtime_risk_limit_policy.yaml：定义风险限额。
- circuit_breaker_policy.yaml：定义熔断策略。
- paper_runtime_permission_policy.yaml：定义纸面运行许可规则。
- execution_risk_gap_policy.yaml：定义 blocking / critical / high / medium / low gap。
- execution_risk_hard_negative_rules.yaml：定义无 P07 handoff、无报价、报价冲突、流动性不足、滑点过高、安全风险、失效触发、熔断、重复仓位、自动实盘等阻断。
- execution_risk_state_machine.yaml：定义 P08 全状态机。
- execution_risk_trace_requirements.yaml：定义 quote trace、security trace、risk limit trace、permission trace、handoff trace。
- p08_acceptance_criteria.md：定义 P08_READY、P08_READY_WITH_GAPS、P08_REJECTED、P08_BLOCKED。
- p08_storage_constitution.md：定义系统文件与运行数据目录。
- p08_test_matrix.yaml：定义至少 18 个测试场景。
- p08_report_model.yaml：定义 P08 人类可读报告。
- p08_review_checklist.md：定义审计清单。
- her_p08_execution_protocol.md：定义 HER 执行 P08 的步骤和禁止事项。

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. P08_READY / P08_READY_WITH_GAPS / P08_REJECTED / P08_BLOCKED 判断
4. quote_snapshot 摘要
5. quote_consistency 摘要
6. liquidity_depth 摘要
7. slippage_estimation 摘要
8. execution_cost_model 摘要
9. security_recheck 摘要
10. sellability_risk 摘要
11. freshness_recheck 摘要
12. invalidation_precheck 摘要
13. runtime_risk_limit 摘要
14. position_uniqueness 摘要
15. circuit_breaker 摘要
16. paper_runtime_permission 摘要
17. paper_runtime_data_request_packet 摘要
18. p08_to_paper_runtime_handoff_packet 摘要
19. P08 阻断规则摘要
20. P08 测试矩阵摘要
21. 当前缺口清单
22. 是否达到轻量机构级 P08 v3.0

最终验收标准：
只有当 P08 具备 execution risk input manifest、P07 candidate validity check、quote snapshot、quote consistency、liquidity depth、slippage estimation、execution cost model、security recheck、sellability risk、freshness recheck、invalidation precheck、wallet delta refresh requirement、runtime risk limits、position uniqueness、circuit breaker、paper entry simulation plan、paper runtime permission、block reason、refresh request、paper runtime data request、P08 handoff contract、gap policy、hard negative rules、state machine、trace requirements、acceptance criteria、storage constitution、test matrix、report model、HER execution protocol，并且 P08 不能执行交易、不能钱包签名、不能绕过 Paper-only Runtime、不能允许 live execution 时，才允许标记为 P08_READY。
```

---

# 36. 当前是否达到专业化标准

## 判断

这一版 P08 达到：

```text
专业化
轻量机构水准
一次性把阶段应有数据补全
不是最小版本
不是下单器
不是纸面交易运行器
```

P08 被明确升级为：

```text
执行前风控层
报价一致性层
流动性深度层
滑点费用层
安全复查层
失效条件复查层
运行风险限额层
纸面运行许可层
Paper-only Runtime 交接层
```

---

# 37. 本版补齐的关键能力

|能力|是否补齐|
|---|---|
|Execution Risk Input Manifest|已补齐|
|P07 Candidate Validity Check|已补齐|
|Quote Snapshot|已补齐|
|Quote Consistency|已补齐|
|Liquidity Depth|已补齐|
|Slippage Estimation|已补齐|
|Execution Cost Model|已补齐|
|Security Recheck|已补齐|
|Sellability Risk|已补齐|
|Freshness Recheck|已补齐|
|Invalidation Precheck|已补齐|
|Wallet Delta Refresh Requirement|已补齐|
|Runtime Risk Limit|已补齐|
|Position Uniqueness|已补齐|
|Circuit Breaker|已补齐|
|Paper Entry Simulation Plan|已补齐|
|Paper Runtime Permission|已补齐|
|Block Reason|已补齐|
|Refresh Request|已补齐|
|Paper Runtime Data Request|已补齐|
|P08 Handoff|已补齐|
|Test Matrix|已补齐|
|HER Execution Protocol|已补齐|

---

# 38. 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|真实 quote / security API 字段未对齐|P08 已定义需求|Runner / Tool Binding 处理|
|滑点模型初始阈值未回测|已定义 schema 和 policy|P09 / P10 校准|
|费用模型可能不精确|已定义成本模型|Paper Runtime 记录后校准|
|wallet delta refresh 需要 P03/P04 联动|已定义刷新请求|Runtime / Runner 编排|
|熔断状态需要真实 runtime state|已定义输入|Paper Runtime 阶段建立|
|P08 不负责持仓记录|已明确边界|Paper-only Runtime 处理|
|P08 不负责失败复盘|已明确边界|P09 Review Replay 处理|
|P08 handoff 未联调|需要 Paper Runtime|下一阶段展开 Paper-only Runtime 或 P09|

---

# 本次认知升级点

1. **P08 的本质不是执行器，而是执行前风控许可层。**
    
2. **P07 的 PAPER_CANDIDATE 必须经过 P08 才能进入纸面运行。**
    
3. **纸面运行也必须检查报价、流动性、滑点、费用和安全。**  
    否则纸面收益会严重失真。
    
4. **P08 必须重新检查当前数据新鲜度。**  
    P07 的策略判断可能已经过期。
    
5. **失效条件必须在执行前复查。**  
    P07 绑定的 invalidation 如果已触发，P08 必须阻断。
    
6. **风险熔断属于 P08 的核心职责。**  
    连续失败、日亏损、重复持仓、数据失败率都应在这里阻断新增纸面样本。
    
7. **PAPER_RUNTIME_ALLOWED 不是 LIVE_EXECUTION_ALLOWED。**  
    P08 只能交接给 Paper-only Runtime，不允许真实下单。
    
8. **P08 的输出必须可复盘。**  
    每次允许、暂停、阻断都必须有报价、安全、滑点、风险限额和失效条件记录。