# P02 Source Data Fact Controller 专业版 v3.0

## 数据事实接收、标准化、质量治理与下游事实交接控制器

## 0. 先修正定位

上一阶段 P01 已经被升级为：

```text
候选主数据治理控制器
```

P02 不能只是：

```text
数据采集脚本
GMGN 字段读取器
行情补全模块
```

P02 的专业定位应该是：

```text
把 P01 交接过来的 Candidate Master Record 和 P02 Data Request Packet，
转化为可追踪、可校验、可标准化、可快照、可评分、可交接的 Source Data Fact Package。
```

一句话定义：

> **P01 负责“候选是谁”。**  
> **P02 负责“围绕这个候选，系统现在掌握了哪些事实数据，这些事实是否完整、可信、新鲜、冲突、可追踪、可交接”。**

P02 不能生成证据。  
P02 不能判断钱包角色。  
P02 不能判断筹码结构。  
P02 不能判断场景。  
P02 不能输出策略准入。  
P02 不能进入 paper runtime。  
P02 不能自动实盘。

---

# 1. P02 阶段核心目标

P02 必须一次性解决 12 个问题：

|编号|问题|P02 必须输出|
|---|---|---|
|1|这个 candidate 的基础事实是否补全？|`token_fact_record`|
|2|token / pair / pool 身份是否一致？|`identity_reconciliation_record`|
|3|市值、价格、流动性是否有多源冲突？|`market_reconciliation_record`|
|4|安全字段是否可用？|`security_fact_record`|
|5|钱包、持有人、交易事实是否可供 P03 使用？|`wallet_fact_seed_record`|
|6|K 线和成交事实是否可供后续结构阶段使用？|`market_structure_fact_record`|
|7|原始数据是否保存？|`raw_data_manifest`|
|8|标准化数据是否生成？|`normalized_fact_package`|
|9|字段质量、新鲜度、冲突是否清楚？|`data_quality_report`|
|10|哪些字段缺失、哪些字段只能弱使用？|`data_gap_report` / `field_usage_limitations`|
|11|下游 P03 应该读取什么？|`p03_wallet_entity_data_request_packet`|
|12|是否可以交接给 P03？|`p02_to_p03_handoff_packet`|

---

# 2. P02 的专业角色模型

P02 应该按 7 个角色设计：

|角色|负责问题|输出|
|---|---|---|
|数据接收官|从 P01 接收候选和数据请求|`p02_input_manifest`|
|原始数据保管官|raw 数据是否保存、可追溯|`raw_data_manifest`|
|标准化工程师|多源字段转为统一事实模型|`normalized_fact_package`|
|数据质量官|完整性、新鲜度、一致性、冲突|`data_quality_report`|
|来源对账官|GMGN / OKX / 链上数据是否冲突|`source_reconciliation_report`|
|下游事实交接官|给 P03 钱包实体层准备数据|`p02_to_p03_handoff_packet`|
|审计官|确保每个事实可 trace / acceptance / handoff|`p02_audit_report`|

---

# 3. P02 底层方法论

## 3.1 Source of Truth 分层原则

P02 不能简单相信单一数据源。

不同事实类型应有不同来源优先级：

|事实类型|优先级原则|
|---|---|
|token address / chain|P01 主键优先|
|pair / pool|GMGN + 链上对账|
|price / market cap|GMGN + OKX quote + 链上估算对账|
|liquidity|DEX / GMGN / pool 数据对账|
|security|OKX Security + 链上权限检查|
|wallet / holder|GMGN 钱包数据 + holder snapshot|
|transaction|GMGN transaction + 链上 raw tx|
|K 线|标准 OHLCV 来源 + 时间窗口对齐|

P02 的目标不是判断哪个源“永远正确”，而是记录：

```text
source_used
source_priority
source_conflict
preferred_source
confidence_status
downstream_usage_limit
```

---

## 3.2 Raw / Normalized 分离原则

P02 必须严格分离：

```text
raw_data：原始数据，只保存，不解释，不覆盖
normalized_fact：标准化事实，可供下游读取
quality_report：事实质量、缺口、冲突、新鲜度
```

禁止把 raw、normalized、analysis 混在一个文件里。

---

## 3.3 Fact，不是 Evidence 原则

P02 只输出事实：

```text
某钱包当前持仓 X
某 token 当前市值 X
某 pool 流动性 X
某字段来自 GMGN
某字段与 OKX 报价偏差 X%
```

P02 不输出：

```text
这是结构钱包
主导侧还在
筹码未派发
二段扩张
可以买
```

这些属于 P03-P07。

---

## 3.4 多时间点快照原则

P02 不能只保存“当前数据”。

必须至少区分：

```text
discovery_snapshot：P01 发现时上下文
p02_collection_snapshot：P02 采集时上下文
latest_fact_snapshot：当前标准化事实
```

否则后续会用当前数据错误解释发现时状态。

---

# 4. P02 必须建立的核心对象

## 4.1 对象总表

|对象|作用|
|---|---|
|`P02 Input Manifest`|记录从 P01 接收了什么|
|`Raw Data Manifest`|记录原始数据来源和保存位置|
|`Source Pull Record`|每次数据源请求记录|
|`Token Fact Record`|token 基础事实|
|`Pair Pool Fact Record`|pair / pool / DEX / liquidity 事实|
|`Market Fact Record`|price / market cap / volume / holder 事实|
|`Security Fact Record`|mint / freeze / blacklist / honeypot / transfer restriction|
|`Wallet Fact Seed Record`|给 P03 的钱包事实种子|
|`Holder Snapshot Fact`|持有人分布快照|
|`Transaction Fact Seed`|交易事实种子|
|`Market Structure Fact Seed`|K 线、成交量、基础结构事实|
|`Source Reconciliation Record`|多源对账|
|`Data Quality Record`|数据质量评分|
|`Data Gap Record`|缺口登记|
|`Data Conflict Record`|冲突登记|
|`Freshness Record`|新鲜度记录|
|`P03 Data Request Packet`|给 P03 的数据交接请求|
|`P02 Handoff Packet`|P02 → P03 标准交接包|

---

# 5. P02 输入：必须读取什么

P02 不能自由读取 P01 文件，必须从 Handoff 进入。

```yaml
p02_required_inputs:
  from_p01:
    - p01_to_p02_handoff_packet
    - candidate_master_records
    - p02_data_request_packet
    - candidate_gap_report
    - candidate_limitation_tags

  from_control_planes:
    - trace_handoff_packet
    - acceptance_result_packet
    - handoff_packet
    - downstream_read_instruction
    - field_usage_permission_packet
    - limitation_transfer_packet
    - governance_handoff_packet
    - data_plane_handoff_packet

  required_contracts:
    - p02_input_contract
    - p02_output_contract
    - data_source_registry_contract
    - field_dictionary_contract
    - raw_data_contract
    - normalized_fact_contract
```

P02 启动前必须确认：

```text
P01 已验收
P01 handoff 已生成
P01 没有阻断状态
P02 只读取 handoff 授权的候选
所有候选仍保持 paper_only
无 live execution 权限
```

---

# 6. P02 数据源注册专业版

## 6.1 数据源分层

```yaml
p02_data_source_registry:
  primary_sources:
    - source_id: GMGN_TOKEN_PROFILE
      purpose:
        - token_profile
        - pair_profile
        - market_cap
        - holder_summary
        - trade_summary
      reliability: B
      freshness_requirement_seconds: 60

    - source_id: GMGN_WALLET_PROFILE
      purpose:
        - wallet_rows
        - holder_wallets
        - wallet_trade_rows
        - top_trader_rows
      reliability: B
      freshness_requirement_seconds: 180

    - source_id: OKX_QUOTE
      purpose:
        - price_cross_check
        - quote_consistency
        - liquidity_reference
      reliability: B
      freshness_requirement_seconds: 30

    - source_id: OKX_SECURITY
      purpose:
        - contract_security
        - transfer_risk
        - permission_risk
      reliability: B
      freshness_requirement_seconds: 600

    - source_id: CHAIN_RAW
      purpose:
        - transaction_validation
        - token_identity_validation
        - pool_validation
        - authority_validation
      reliability: A
      freshness_requirement_seconds: 300

  secondary_sources:
    - source_id: KLINE_PROVIDER
      purpose:
        - ohlcv
        - volume
        - candle_sequence
      reliability: B
      freshness_requirement_seconds: 60

    - source_id: HOLDER_SNAPSHOT_PROVIDER
      purpose:
        - holder_distribution
        - top_holder_snapshot
      reliability: B
      freshness_requirement_seconds: 300

    - source_id: LEGACY_RUNTIME_REFERENCE
      purpose:
        - historical_reference
        - replay_reference
        - migration_reference
      reliability: C
      freshness_requirement_seconds: null
      usage_limit: OBSERVE_ONLY

    - source_id: MANUAL_ANNOTATION
      purpose:
        - human_note
        - operator_context
      reliability: C
      usage_limit: CONTEXT_ONLY
```

---

# 7. P02 标准事实数据包

## 7.1 Source Data Fact Package

这是 P02 的核心资产。

```yaml
source_data_fact_package:
  package_id: string
  candidate_id: string
  token_address: string
  chain: string
  generated_at: datetime
  p02_run_id: string

  input_reference:
    p01_handoff_packet_id: string
    p02_data_request_packet_id: string
    candidate_trace_id: string

  raw_data:
    raw_data_manifest_path: string
    raw_source_pull_records_path: string
    raw_payload_paths: list

  normalized_facts:
    token_fact_record_path: string
    pair_pool_fact_record_path: string
    market_fact_record_path: string
    security_fact_record_path: string
    wallet_fact_seed_path: string
    holder_snapshot_fact_path: string
    transaction_fact_seed_path: string
    market_structure_fact_seed_path: string

  quality:
    data_quality_report_path: string
    freshness_report_path: string
    conflict_report_path: string
    gap_report_path: string

  downstream:
    p03_data_request_packet_path: string
    p02_to_p03_handoff_packet_path: string

  constraints:
    no_evidence_generation: true
    no_wallet_role_classification: true
    no_strategy_gate: true
    no_paper_runtime: true
    live_execution_allowed: false
```

---

# 8. Raw Data Manifest

P02 必须保存 raw 索引，而不是只保存标准化结果。

```yaml
raw_data_manifest:
  manifest_id: string
  candidate_id: string
  token_address: string
  chain: string
  generated_at: datetime

  raw_records:
    - raw_record_id: string
      source_id: string
      source_type:
        - API_RESPONSE
        - AGENT_SKILL_OUTPUT
        - CHAIN_QUERY
        - CSV_IMPORT
        - LEGACY_REFERENCE
      collected_at: datetime
      request_params: object
      response_status: string
      raw_payload_path: string
      checksum: string
      parser_version: string
      immutable: true

  coverage:
    token_profile_raw_available: boolean
    wallet_raw_available: boolean
    holder_raw_available: boolean
    transaction_raw_available: boolean
    kline_raw_available: boolean
    security_raw_available: boolean
    quote_raw_available: boolean

  audit:
    raw_files_count: integer
    missing_raw_sources: list
    failed_source_pulls: list
```

---

# 9. Source Pull Record

每次请求都要记录，不然无法追踪数据为什么缺失。

```yaml
source_pull_record:
  pull_id: string
  candidate_id: string
  source_id: string
  pull_started_at: datetime
  pull_finished_at: datetime | null

  request:
    query_type: string
    query_params: object
    expected_fields: list

  response:
    response_status:
      - SUCCESS
      - PARTIAL_SUCCESS
      - EMPTY
      - RATE_LIMITED
      - ERROR
      - SOURCE_UNAVAILABLE
    response_latency_ms: integer | null
    raw_payload_path: string | null
    error_message: string | null

  quality:
    source_freshness_status: string
    field_coverage_score: number
    source_pull_quality:
      - SOURCE_PULL_COMPLETE
      - SOURCE_PULL_PARTIAL
      - SOURCE_PULL_FAILED
      - SOURCE_PULL_STALE

  downstream_effect:
    missing_fields_created: list
    conflict_fields_created: list
    refresh_required: boolean
```

---

# 10. Token Fact Record

```yaml
token_fact_record:
  candidate_id: string
  token_address: string
  chain: string

  token_identity:
    token_symbol: string | null
    token_name: string | null
    token_decimals: integer | null
    token_standard: string | null
    token_supply_total: number | null
    token_supply_circulating: number | null
    deployer_address: string | null
    creator_address: string | null
    launch_time: datetime | null

  authority_status:
    mint_authority_status:
      - DISABLED
      - ENABLED
      - UNKNOWN
    freeze_authority_status:
      - DISABLED
      - ENABLED
      - UNKNOWN
    owner_permission_status:
      - RENOUNCED
      - ACTIVE
      - UNKNOWN

  source:
    preferred_source_id: string
    supporting_source_ids: list
    source_conflict_detected: boolean

  quality:
    identity_fact_quality:
      - HIGH
      - USABLE
      - USABLE_WITH_GAPS
      - LOW
      - REJECTED
    missing_fields: list
    conflict_fields: list

  trace:
    field_trace_ids: list
    raw_record_ids: list
```

---

# 11. Pair / Pool Fact Record

```yaml
pair_pool_fact_record:
  candidate_id: string
  token_address: string
  chain: string

  pair_pool_identity:
    pair_address: string | null
    pool_address: string | null
    dex_name: string | null
    quote_token_address: string | null
    quote_token_symbol: string | null
    base_token_address: string | null
    pool_created_at: datetime | null
    pool_age_seconds: integer | null

  liquidity:
    liquidity_usd: number | null
    liquidity_base: number | null
    liquidity_quote: number | null
    liquidity_change_5m_pct: number | null
    liquidity_change_1h_pct: number | null
    liquidity_lock_status: string | null

  pool_status:
    pool_confirmed: boolean
    multi_pool_detected: boolean
    primary_pool_selected: boolean
    pool_conflict_status:
      - NO_CONFLICT
      - MULTI_POOL
      - POOL_MISSING
      - POOL_CONFLICTED
      - UNKNOWN

  quality:
    pool_fact_quality: string
    missing_fields: list
    conflict_fields: list
    downstream_limitations: list
```

---

# 12. Market Fact Record

```yaml
market_fact_record:
  candidate_id: string
  token_address: string
  chain: string
  snapshot_time: datetime

  price_market_cap:
    price_usd: number | null
    current_market_cap_usd: number | null
    fdv_usd: number | null
    discovery_market_cap_usd: number | null
    market_cap_change_from_discovery_pct: number | null

  volume_trade:
    volume_5m_usd: number | null
    volume_15m_usd: number | null
    volume_1h_usd: number | null
    buy_volume_5m_usd: number | null
    sell_volume_5m_usd: number | null
    trade_count_5m: integer | null
    trade_count_1h: integer | null
    buy_sell_ratio_5m: number | null

  holder_summary:
    holder_count: integer | null
    top_holder_pct: number | null
    top_10_holder_pct: number | null
    top_20_holder_pct: number | null

  source_reconciliation:
    gmgn_price_usd: number | null
    okx_quote_price_usd: number | null
    chain_estimated_price_usd: number | null
    quote_deviation_pct: number | null
    quote_consistency_status:
      - CONSISTENT
      - MINOR_DEVIATION
      - MAJOR_DEVIATION
      - SOURCE_MISSING
      - UNKNOWN

  quality:
    market_fact_quality: string
    stale_fields: list
    missing_fields: list
    conflicted_fields: list
    downstream_limitations: list
```

---

# 13. Security Fact Record

P02 必须提供安全事实，但不能做最终执行风控。

```yaml
security_fact_record:
  candidate_id: string
  token_address: string
  chain: string
  checked_at: datetime

  authority_risks:
    mint_authority_risk:
      - NONE
      - PRESENT
      - UNKNOWN
    freeze_authority_risk:
      - NONE
      - PRESENT
      - UNKNOWN
    owner_permission_risk:
      - NONE
      - PRESENT
      - UNKNOWN

  transfer_risks:
    blacklist_risk:
      - NONE
      - DETECTED
      - UNKNOWN
    transfer_restriction_risk:
      - NONE
      - DETECTED
      - UNKNOWN
    honeypot_risk:
      - NONE
      - DETECTED
      - UNKNOWN
    tax_risk:
      - NONE
      - HIGH
      - UNKNOWN

  liquidity_risks:
    liquidity_lock_status:
      - LOCKED
      - UNLOCKED
      - UNKNOWN
    lp_removal_risk:
      - LOW
      - MEDIUM
      - HIGH
      - UNKNOWN

  quality:
    security_fact_quality:
      - SECURITY_FACT_HIGH
      - SECURITY_FACT_USABLE
      - SECURITY_FACT_WITH_GAPS
      - SECURITY_FACT_LOW
      - SECURITY_FACT_REJECTED
    missing_security_fields: list
    security_source_ids: list

  downstream:
    execution_risk_must_recheck: true
    p08_final_authority_required: true
```

注意：

```text
P02 安全事实不等于最终安全通过。
P08 Execution Risk 必须重新检查。
```

---

# 14. Wallet Fact Seed Record

P02 只提供钱包事实种子，不能分类钱包角色。

```yaml
wallet_fact_seed_record:
  candidate_id: string
  token_address: string
  generated_at: datetime

  wallet_rows:
    wallet_rows_path: string | null
    wallet_row_count: integer
    top_holder_rows_path: string | null
    trader_rows_path: string | null

  wallet_seed_fields:
    - wallet_address
    - current_holding_amount
    - current_holding_pct
    - first_buy_time
    - first_buy_amount
    - total_buy_amount
    - total_sell_amount
    - realized_profit
    - unrealized_profit
    - transaction_count
    - funding_source_address_if_available

  coverage:
    has_top_holders: boolean
    has_trader_rows: boolean
    has_wallet_transactions: boolean
    has_funding_source: boolean
    has_historical_wallet_profile: boolean

  quality:
    wallet_fact_seed_quality:
      - WALLET_FACT_READY
      - WALLET_FACT_READY_WITH_GAPS
      - WALLET_FACT_LOW
      - WALLET_FACT_UNUSABLE
    missing_wallet_fields: list
    p03_required_backfill: list

  forbidden:
    - wallet_role_classification
    - same_source_group_claim
    - dominant_side_claim
    - chip_control_claim
```

---

# 15. Holder Snapshot Fact

```yaml
holder_snapshot_fact:
  candidate_id: string
  token_address: string
  snapshot_time: datetime

  holder_distribution:
    holder_count: integer | null
    top_1_holder_pct: number | null
    top_5_holder_pct: number | null
    top_10_holder_pct: number | null
    top_20_holder_pct: number | null
    lp_holder_pct: number | null
    contract_holder_pct: number | null

  holder_rows:
    holder_rows_path: string | null
    row_count: integer
    fields_available:
      - holder_address
      - holding_amount
      - holding_pct
      - holding_value_usd
      - first_seen_time
      - last_activity_time

  quality:
    snapshot_freshness_status:
      - FRESH
      - ACCEPTABLE
      - STALE
      - EXPIRED
      - UNKNOWN
    holder_snapshot_quality: string
    missing_fields: list
```

---

# 16. Transaction Fact Seed

```yaml
transaction_fact_seed:
  candidate_id: string
  token_address: string
  transaction_window:
    start_time: datetime | null
    end_time: datetime | null
    interval_seconds: integer | null

  transaction_rows:
    transaction_rows_path: string | null
    row_count: integer

  available_event_types:
    - BUY
    - SELL
    - TRANSFER_IN
    - TRANSFER_OUT
    - ADD_LIQUIDITY
    - REMOVE_LIQUIDITY
    - UNKNOWN

  transaction_fields_available:
    - tx_hash
    - block_time
    - wallet_address
    - side
    - amount_token
    - amount_usd
    - price_usd
    - pool_address
    - counterparty_address
    - gas_fee
    - source

  quality:
    transaction_fact_quality: string
    missing_transaction_fields: list
    p03_p04_required_backfill: list
```

---

# 17. Market Structure Fact Seed

P02 只提供 K 线与成交基础事实，不判断结构。

```yaml
market_structure_fact_seed:
  candidate_id: string
  token_address: string

  candle_data:
    candle_intervals_available:
      - 1m
      - 5m
      - 15m
      - 1h
    candle_rows_path: string | null
    earliest_candle_time: datetime | null
    latest_candle_time: datetime | null

  ohlcv_fields:
    - open
    - high
    - low
    - close
    - volume
    - turnover_usd
    - buy_volume
    - sell_volume
    - trade_count

  derived_basic_fields:
    price_change_5m_pct: number | null
    price_change_1h_pct: number | null
    volume_change_5m_pct: number | null
    volatility_basic: number | null

  quality:
    kline_fact_quality: string
    missing_intervals: list
    stale_candles: boolean
    downstream_limitations:
      - NO_STRUCTURE_CLAIM
      - SCENARIO_CONTROLLER_MUST_RECALCULATE
```

---

# 18. Source Reconciliation Record

P02 必须对账，不是简单合并字段。

```yaml
source_reconciliation_record:
  candidate_id: string
  token_address: string
  generated_at: datetime

  reconciled_fields:
    - field_key: string
      source_values:
        - source_id: string
          value: any
          collected_at: datetime
          freshness_status: string
      preferred_source_id: string | null
      preferred_value: any
      conflict_detected: boolean
      deviation_pct: number | null
      reconciliation_status:
        - AGREED
        - MINOR_CONFLICT
        - MAJOR_CONFLICT
        - SINGLE_SOURCE_ONLY
        - NO_SOURCE_AVAILABLE

  conflict_summary:
    conflicted_fields: list
    major_conflicts: list
    downstream_limitations: list

  policy:
    silent_overwrite_allowed: false
    average_conflicting_values_allowed: false
    conflict_must_be_propagated: true
```

---

# 19. Data Quality Record

```yaml
data_quality_record:
  candidate_id: string
  generated_at: datetime

  quality_dimensions:
    completeness_score: number
    freshness_score: number
    consistency_score: number
    traceability_score: number
    source_reliability_score: number
    replayability_score: number
    normalization_score: number

  weighted_quality_score: number

  data_quality_status:
    - DATA_FACT_HIGH_CONFIDENCE
    - DATA_FACT_USABLE
    - DATA_FACT_USABLE_WITH_GAPS
    - DATA_FACT_LOW_CONFIDENCE
    - DATA_FACT_UNUSABLE

  blocking_issues: list
  critical_gaps: list
  high_gaps: list
  medium_gaps: list
  low_gaps: list

  downstream_permission:
    p03_wallet_entity_allowed: boolean
    p04_chip_structure_allowed: false
    p05_evidence_allowed: false
    p07_strategy_gate_allowed: false
    paper_runtime_allowed: false
```

---

# 20. Freshness Policy

```yaml
p02_freshness_policy:
  quote_price:
    fresh_seconds: 30
    acceptable_seconds: 90
    stale_seconds: 300

  liquidity:
    fresh_seconds: 60
    acceptable_seconds: 180
    stale_seconds: 600

  wallet_rows:
    fresh_seconds: 180
    acceptable_seconds: 600
    stale_seconds: 1800

  holder_snapshot:
    fresh_seconds: 300
    acceptable_seconds: 900
    stale_seconds: 3600

  security_scan:
    fresh_seconds: 600
    acceptable_seconds: 1800
    stale_seconds: 7200

  kline:
    fresh_rule: latest_candle_must_be_within_current_interval

  legacy_reference:
    always_stale_for_live_decision: true
    usage_limit: OBSERVE_ONLY
```

---

# 21. P02 Gap Policy

```yaml
p02_gap_policy:
  BLOCKING_GAP:
    result: P02_BLOCKED
    examples:
      - p01_handoff_missing
      - token_address_missing
      - chain_missing
      - no_raw_data_saved
      - no_trace
      - live_execution_requested

  CRITICAL_GAP:
    result: P02_REJECTED
    examples:
      - token_identity_unresolved
      - all_primary_sources_failed
      - source_data_untraceable
      - output_contract_missing

  HIGH_GAP:
    result: P02_READY_WITH_GAPS
    downstream_permission: P03_LIMITED
    examples:
      - wallet_rows_missing
      - holder_snapshot_missing
      - pool_identity_missing
      - security_scan_missing
      - major_market_cap_conflict

  MEDIUM_GAP:
    result: P02_READY_WITH_GAPS
    downstream_permission: P03_ALLOWED_WITH_LIMITATIONS
    examples:
      - discovery_market_cap_missing
      - token_age_missing
      - quote_source_missing
      - partial_transaction_rows

  LOW_GAP:
    result: P02_READY_WITH_GAPS
    downstream_permission: P03_ALLOWED_WITH_NOTE
    examples:
      - token_name_missing
      - source_rank_missing
      - minor_quote_deviation
```

---

# 22. P02 Hard Negative Rules

```yaml
p02_hard_negative_rules:
  - rule_id: P02_BLOCK_001
    name: 未读取 P01 handoff
    condition: p01_to_p02_handoff_packet_missing == true
    result: P02_BLOCKED
    reason: P02 不能绕过 P01 / Handoff 启动

  - rule_id: P02_BLOCK_002
    name: 无 token 主键
    condition: token_address is null or chain is null
    result: P02_REJECTED
    reason: 无法建立数据事实主键

  - rule_id: P02_BLOCK_003
    name: raw 数据未保存
    condition: raw_data_manifest_missing == true
    result: P02_BLOCKED
    reason: 无 raw 不能建立可审计事实

  - rule_id: P02_BLOCK_004
    name: 所有主要数据源失败
    condition: all_primary_sources_failed == true
    result: P02_REJECTED
    reason: 无可用事实来源

  - rule_id: P02_BLOCK_005
    name: 静默覆盖冲突字段
    condition: conflict_detected == true and conflict_report_missing == true
    result: P02_BLOCKED
    reason: 多源冲突必须显式传递

  - rule_id: P02_BLOCK_006
    name: P02 输出证据或策略
    condition: output_contains in [evidence_strength, scenario_claim, strategy_signal, paper_ready]
    result: P02_BLOCKED
    reason: P02 越权

  - rule_id: P02_BLOCK_007
    name: 自动实盘路径
    condition: live_execution_requested == true or live_execution_allowed == true
    result: P02_BLOCKED
    reason: 当前系统禁止自动实盘

  - rule_id: P02_BLOCK_008
    name: 无 trace 标准化
    condition: normalized_fact_created == true and field_trace_missing == true
    result: P02_BLOCKED
    reason: 标准化事实必须可追踪
```

---

# 23. P02 状态机专业版

```yaml
p02_source_data_fact_state_machine:
  states:
    - P02_UNINITIALIZED
    - P02_CONTEXT_LOADED
    - P02_HANDOFF_READ
    - P02_INPUT_MANIFEST_BUILT
    - P02_SOURCE_PLAN_BUILT
    - P02_RAW_PULL_RUNNING
    - P02_RAW_DATA_SAVED
    - P02_SOURCE_PULL_INDEXED
    - P02_NORMALIZATION_RUNNING
    - P02_NORMALIZED_FACTS_BUILT
    - P02_RECONCILIATION_RUNNING
    - P02_RECONCILIATION_COMPLETED
    - P02_QUALITY_SCORED
    - P02_GAP_ANALYZED
    - P02_P03_DATA_REQUEST_BUILT
    - P02_READY_FOR_ACCEPTANCE
    - P02_ACCEPTANCE_READY
    - P02_READY_FOR_P03_HANDOFF
    - P02_READY_WITH_GAPS
    - P02_REJECTED
    - P02_BLOCKED

  transitions:
    - from: P02_HANDOFF_READ
      to: P02_INPUT_MANIFEST_BUILT
      condition: p01_handoff_valid == true

    - from: P02_INPUT_MANIFEST_BUILT
      to: P02_SOURCE_PLAN_BUILT
      condition: p02_data_request_packet_loaded == true

    - from: P02_SOURCE_PLAN_BUILT
      to: P02_RAW_PULL_RUNNING
      condition: source_plan_has_at_least_one_primary_source == true

    - from: P02_RAW_PULL_RUNNING
      to: P02_RAW_DATA_SAVED
      condition: raw_data_manifest_created == true

    - from: P02_RAW_DATA_SAVED
      to: P02_NORMALIZATION_RUNNING
      condition: raw_records_indexed == true

    - from: P02_NORMALIZATION_RUNNING
      to: P02_NORMALIZED_FACTS_BUILT
      condition: normalized_fact_package_created == true

    - from: P02_NORMALIZED_FACTS_BUILT
      to: P02_RECONCILIATION_RUNNING
      condition: multi_source_fields_detected == true

    - from: P02_RECONCILIATION_RUNNING
      to: P02_RECONCILIATION_COMPLETED
      condition: source_reconciliation_record_created == true

    - from: P02_RECONCILIATION_COMPLETED
      to: P02_QUALITY_SCORED
      condition: data_quality_record_created == true

    - from: P02_QUALITY_SCORED
      to: P02_GAP_ANALYZED
      condition: data_gap_report_created == true

    - from: P02_GAP_ANALYZED
      to: P02_P03_DATA_REQUEST_BUILT
      condition: p03_data_request_packet_created == true

    - from: P02_P03_DATA_REQUEST_BUILT
      to: P02_READY_FOR_ACCEPTANCE
      condition: p02_output_contract_ready == true

    - from: P02_READY_FOR_ACCEPTANCE
      to: P02_ACCEPTANCE_READY
      condition: acceptance_status in [ACCEPTANCE_READY, ACCEPTANCE_READY_WITH_GAPS]

    - from: P02_ACCEPTANCE_READY
      to: P02_READY_FOR_P03_HANDOFF
      condition: p02_to_p03_handoff_packet_created == true
```

---

# 24. P03 Data Request Packet

P02 必须告诉 P03 钱包实体层可以读取什么、还缺什么。

```yaml
p03_wallet_entity_data_request_packet:
  packet_id: string
  from_controller: P02_SOURCE_DATA_FACT_CONTROLLER
  to_controller: P03_WALLET_ENTITY_CONTROLLER
  generated_at: datetime

  candidate_scope:
    candidate_ids: list
    token_addresses: list
    chain: string

  available_wallet_fact_seeds:
    wallet_fact_seed_path: string
    holder_snapshot_path: string
    transaction_fact_seed_path: string
    wallet_row_count_by_candidate: object

  p03_required_processing:
    - wallet_entity_resolution
    - funding_source_extraction
    - same_source_candidate_detection
    - sync_buy_candidate_detection
    - sync_sell_candidate_detection
    - wallet_role_initial_classification

  missing_or_limited_inputs:
    missing_wallet_rows: list
    missing_funding_source: list
    stale_holder_snapshots: list
    partial_transaction_rows: list

  usage_limitations:
    - FACTS_ONLY
    - NO_WALLET_ROLE_CONFIRMED
    - NO_DOMINANT_SIDE_CLAIM
    - NO_CHIP_CONTROL_CLAIM
    - NO_EVIDENCE
    - NO_STRATEGY_GATE
    - LIVE_EXECUTION_FORBIDDEN

  field_usage_permissions:
    full_use_fields: list
    weak_use_only_fields: list
    observe_only_fields: list
    do_not_use_fields: list
```

---

# 25. P02 Handoff Packet 专业版

```yaml
p02_to_p03_handoff_packet:
  packet_id: string
  packet_type: P02_TO_P03_SOURCE_DATA_FACT_HANDOFF
  generated_at: datetime

  route:
    from_controller: P02_SOURCE_DATA_FACT_CONTROLLER
    to_controller: P03_WALLET_ENTITY_CONTROLLER

  upstream_control:
    p01_handoff_packet_id: string
    p02_acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    handoff_trace_id: string

  candidate_scope:
    candidate_count_total: integer
    candidate_count_data_ready: integer
    candidate_count_ready_with_gaps: integer
    candidate_count_rejected: integer
    candidate_count_blocked: integer

  fact_package:
    source_data_fact_package_index_path: string
    raw_data_manifest_path: string
    normalized_fact_package_path: string
    source_reconciliation_report_path: string
    data_quality_report_path: string
    data_gap_report_path: string
    data_conflict_report_path: string

  normalized_fact_paths:
    token_fact_records_path: string
    pair_pool_fact_records_path: string
    market_fact_records_path: string
    security_fact_records_path: string
    wallet_fact_seed_records_path: string
    holder_snapshot_fact_path: string
    transaction_fact_seed_path: string
    market_structure_fact_seed_path: string

  p03_data_request:
    p03_wallet_entity_data_request_packet_path: string
    required_p03_tasks: list
    missing_inputs_by_candidate: object

  quality_summary:
    data_quality_distribution: object
    source_pull_quality_distribution: object
    freshness_summary: object
    conflict_summary: object

  limitations:
    - FACTS_ONLY
    - NO_EVIDENCE
    - NO_SCENARIO
    - NO_STRATEGY_GATE
    - NO_RUNTIME
    - LIVE_EXECUTION_FORBIDDEN

  downstream_permission:
    allowed:
      - P03_WALLET_ENTITY_CONTROLLER
    forbidden:
      - P04_CHIP_STRUCTURE_CONTROLLER
      - P05_EVIDENCE_CONTROLLER
      - P06_SCENARIO_RECOGNITION_CONTROLLER
      - P07_STRATEGY_GATE_CONTROLLER
      - PAPER_ONLY_RUNTIME
      - LIVE_EXECUTION

  read_instruction:
    p03_must_read_first:
      - p02_to_p03_handoff_packet
      - p03_wallet_entity_data_request_packet
      - wallet_fact_seed_records
      - holder_snapshot_fact
      - transaction_fact_seed
      - data_quality_report
      - field_usage_permissions
```

---

# 26. P02 文件体系

## 26.1 系统目录

```text
/root/sikk-gmgn/system/phase_controllers/p02_source_data_fact_controller/
```

必须创建：

```text
p02_source_data_fact_controller.yaml
p02_source_data_fact_context.md
p02_input_contract.yaml
p02_output_contract.yaml
p02_data_source_registry.yaml
p02_source_pull_plan_schema.yaml
source_pull_record_schema.yaml
raw_data_manifest_schema.yaml
source_data_fact_package_schema.yaml
token_fact_record_schema.yaml
pair_pool_fact_record_schema.yaml
market_fact_record_schema.yaml
security_fact_record_schema.yaml
wallet_fact_seed_record_schema.yaml
holder_snapshot_fact_schema.yaml
transaction_fact_seed_schema.yaml
market_structure_fact_seed_schema.yaml
source_reconciliation_record_schema.yaml
data_quality_record_schema.yaml
data_freshness_policy.yaml
data_gap_policy.yaml
data_conflict_policy.yaml
p02_hard_negative_rules.yaml
p02_state_machine.yaml
p02_trace_requirements.yaml
p03_data_request_packet_contract.yaml
p02_to_p03_handoff_contract.yaml
p02_acceptance_criteria.md
p02_storage_constitution.md
p02_test_matrix.yaml
p02_report_model.yaml
p02_review_checklist.md
her_p02_execution_protocol.md
```

---

## 26.2 运行数据目录

```text
/root/sikk-gmgn/data/phase_controllers/p02_source_data_fact/
  input_manifest/
  source_pull_plans/
  source_pull_records/
  raw/
    gmgn_token/
    gmgn_wallet/
    okx_quote/
    okx_security/
    chain_raw/
    kline/
    holder_snapshot/
    legacy_reference/
  normalized/
    token_facts/
    pair_pool_facts/
    market_facts/
    security_facts/
    wallet_fact_seed/
    holder_snapshot/
    transaction_fact_seed/
    market_structure_fact_seed/
  reconciliation/
  quality/
  freshness/
  conflicts/
  gaps/
  p03_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/
```

---

# 27. P02 测试矩阵

```yaml
p02_test_matrix:
  - test_id: P02_TEST_001
    name: P01 正常 handoff 输入
    expected_status: P02_READY_FOR_P03_HANDOFF

  - test_id: P02_TEST_002
    name: 缺 P01 handoff
    expected_status: P02_BLOCKED

  - test_id: P02_TEST_003
    name: GMGN token 成功但 OKX quote 缺失
    expected_status: P02_READY_WITH_GAPS
    expected_limitation: QUOTE_CROSS_CHECK_MISSING

  - test_id: P02_TEST_004
    name: 所有主数据源失败
    expected_status: P02_REJECTED

  - test_id: P02_TEST_005
    name: market cap 多源冲突超过阈值
    expected_status: P02_READY_WITH_GAPS
    expected_conflict_record: current_market_cap_usd

  - test_id: P02_TEST_006
    name: raw 数据未保存但 normalized 存在
    expected_status: P02_BLOCKED

  - test_id: P02_TEST_007
    name: wallet rows 缺失
    expected_status: P02_READY_WITH_GAPS
    expected_p03_limitation: WALLET_FACT_SEED_MISSING

  - test_id: P02_TEST_008
    name: security scan 缺失
    expected_status: P02_READY_WITH_GAPS
    expected_downstream_note: P08_MUST_RECHECK_SECURITY

  - test_id: P02_TEST_009
    name: P02 输出 scenario claim
    expected_status: P02_BLOCKED

  - test_id: P02_TEST_010
    name: live execution requested
    expected_status: P02_BLOCKED

  - test_id: P02_TEST_011
    name: legacy reference only
    expected_status: P02_READY_WITH_GAPS
    expected_limitation: OBSERVE_ONLY

  - test_id: P02_TEST_012
    name: field trace missing
    expected_status: P02_BLOCKED
```

---

# 28. P02 报告模型

```yaml
p02_source_data_fact_report:
  report_id: string
  generated_at: datetime
  controller_id: P02_SOURCE_DATA_FACT_CONTROLLER

  summary:
    candidate_count_received: integer
    candidate_count_processed: integer
    candidate_count_ready_for_p03: integer
    candidate_count_ready_with_gaps: integer
    candidate_count_rejected: integer
    candidate_count_blocked: integer

  source_pull_summary:
    source_success_count: integer
    source_partial_count: integer
    source_failed_count: integer
    failed_sources: list

  fact_coverage_summary:
    token_fact_coverage: number
    pool_fact_coverage: number
    market_fact_coverage: number
    security_fact_coverage: number
    wallet_fact_seed_coverage: number
    transaction_fact_coverage: number
    kline_fact_coverage: number

  quality_summary:
    data_quality_distribution: object
    freshness_distribution: object
    conflict_count: integer
    major_conflict_fields: list

  gap_summary:
    blocking_gaps: list
    critical_gaps: list
    high_gaps: list
    medium_gaps: list
    low_gaps: list

  p03_handoff_summary:
    p03_handoff_ready: boolean
    p03_limited_candidates: integer
    p03_required_backfills: list

  compliance:
    evidence_generated: false
    scenario_claim_generated: false
    strategy_signal_generated: false
    paper_runtime_started: false
    live_execution_path_detected: false
```

---

# 29. HER P02 执行协议

```text
HER 执行 P02 时必须按以下顺序：

1. 读取 professional_build_order.md
2. 读取 phase_controller_index.yaml
3. 读取 P02 controller context
4. 读取 P01 → P02 handoff packet
5. 读取 P01 生成的 p02_data_request_packet
6. 读取 Trace / Acceptance / Handoff 输出
7. 建立 P02 input_manifest
8. 根据 P02 data request 生成 source_pull_plan
9. 执行或登记各数据源 pull
10. 保存 raw_data_manifest
11. 建立 source_pull_record
12. 标准化 token_fact_record
13. 标准化 pair_pool_fact_record
14. 标准化 market_fact_record
15. 标准化 security_fact_record
16. 标准化 wallet_fact_seed_record
17. 标准化 holder_snapshot_fact
18. 标准化 transaction_fact_seed
19. 标准化 market_structure_fact_seed
20. 执行 source_reconciliation
21. 生成 data_quality_record
22. 生成 freshness_report
23. 生成 data_conflict_report
24. 生成 data_gap_report
25. 生成 p03_wallet_entity_data_request_packet
26. 写入 P02 trace
27. 生成 p02_source_data_fact_report
28. 生成 p02_to_p03_handoff_packet
29. 执行 P02 acceptance
30. 只允许 handoff 给 P03
```

禁止：

```text
1. 不允许无 P01 handoff 启动 P02
2. 不允许无 raw_data_manifest 生成 normalized facts
3. 不允许静默覆盖冲突字段
4. 不允许把来源质量当成交易质量
5. 不允许生成 evidence
6. 不允许判断 wallet role
7. 不允许判断 chip control
8. 不允许识别 scenario
9. 不允许输出 strategy signal
10. 不允许进入 paper runtime
11. 不允许任何 live execution
```

---

# 30. 给 HER 的专业化任务书

```text
任务名称：重建 P02 Source Data Fact Controller 专业版 v3.0

目标：
在 /root/sikk-gmgn/system/phase_controllers/p02_source_data_fact_controller/ 下重建 P02 Source Data Fact Controller。该控制器不是简单数据采集脚本，也不是 GMGN 字段读取器，而是数据事实接收、标准化、质量治理与下游事实交接控制器。它负责读取 P01 Candidate Intake Controller 输出的 candidate master 和 p02_data_request_packet，围绕每个 candidate 建立 raw 数据保管、normalized facts、source reconciliation、data quality、freshness、gap、conflict、P03 data request 和 P02→P03 handoff。

核心原则：
1. P02 只生产数据事实，不生成证据。
2. P02 不判断钱包角色。
3. P02 不判断筹码结构。
4. P02 不识别交易场景。
5. P02 不做策略准入。
6. P02 不进入 paper runtime。
7. P02 不允许 live execution。
8. P02 必须保存 raw_data_manifest。
9. P02 必须生成 normalized_fact_package。
10. P02 必须显式记录 source conflict，不允许静默覆盖。
11. P02 必须生成 p03_wallet_entity_data_request_packet。
12. P02 只能交接给 P03 Wallet Entity Controller。

需要创建系统目录：
/root/sikk-gmgn/system/phase_controllers/p02_source_data_fact_controller/

需要创建系统文件：
1. p02_source_data_fact_controller.yaml
2. p02_source_data_fact_context.md
3. p02_input_contract.yaml
4. p02_output_contract.yaml
5. p02_data_source_registry.yaml
6. p02_source_pull_plan_schema.yaml
7. source_pull_record_schema.yaml
8. raw_data_manifest_schema.yaml
9. source_data_fact_package_schema.yaml
10. token_fact_record_schema.yaml
11. pair_pool_fact_record_schema.yaml
12. market_fact_record_schema.yaml
13. security_fact_record_schema.yaml
14. wallet_fact_seed_record_schema.yaml
15. holder_snapshot_fact_schema.yaml
16. transaction_fact_seed_schema.yaml
17. market_structure_fact_seed_schema.yaml
18. source_reconciliation_record_schema.yaml
19. data_quality_record_schema.yaml
20. data_freshness_policy.yaml
21. data_gap_policy.yaml
22. data_conflict_policy.yaml
23. p02_hard_negative_rules.yaml
24. p02_state_machine.yaml
25. p02_trace_requirements.yaml
26. p03_data_request_packet_contract.yaml
27. p02_to_p03_handoff_contract.yaml
28. p02_acceptance_criteria.md
29. p02_storage_constitution.md
30. p02_test_matrix.yaml
31. p02_report_model.yaml
32. p02_review_checklist.md
33. her_p02_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/phase_controllers/p02_source_data_fact/
  input_manifest/
  source_pull_plans/
  source_pull_records/
  raw/
    gmgn_token/
    gmgn_wallet/
    okx_quote/
    okx_security/
    chain_raw/
    kline/
    holder_snapshot/
    legacy_reference/
  normalized/
    token_facts/
    pair_pool_facts/
    market_facts/
    security_facts/
    wallet_fact_seed/
    holder_snapshot/
    transaction_fact_seed/
    market_structure_fact_seed/
  reconciliation/
  quality/
  freshness/
  conflicts/
  gaps/
  p03_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/

每个文件要求：
- p02_source_data_fact_controller.yaml：定义 P02 身份、职责、权限、上下游、状态码、禁止事项。
- p02_source_data_fact_context.md：写成 HER 执行前必须读取的 P02 上下文。
- p02_input_contract.yaml：定义 P02 必须读取的 P01 handoff、p02_data_request_packet、candidate master、trace、acceptance、handoff。
- p02_output_contract.yaml：定义 raw manifest、normalized facts、quality、gap、conflict、P03 request、handoff 输出。
- p02_data_source_registry.yaml：定义 GMGN_TOKEN_PROFILE、GMGN_WALLET_PROFILE、OKX_QUOTE、OKX_SECURITY、CHAIN_RAW、KLINE_PROVIDER、HOLDER_SNAPSHOT_PROVIDER、LEGACY_RUNTIME_REFERENCE、MANUAL_ANNOTATION。
- p02_source_pull_plan_schema.yaml：定义每个 candidate 应拉取哪些数据源、字段、优先级、fallback。
- source_pull_record_schema.yaml：定义每次数据源请求记录。
- raw_data_manifest_schema.yaml：定义 raw 数据保管索引。
- source_data_fact_package_schema.yaml：定义 P02 核心事实数据包。
- token_fact_record_schema.yaml：定义 token 基础事实。
- pair_pool_fact_record_schema.yaml：定义 pair / pool / liquidity 事实。
- market_fact_record_schema.yaml：定义 price / market cap / volume / holder summary 事实。
- security_fact_record_schema.yaml：定义安全事实，但不得作为最终执行安全通过。
- wallet_fact_seed_record_schema.yaml：定义给 P03 的钱包事实种子，不得分类钱包角色。
- holder_snapshot_fact_schema.yaml：定义持有人分布快照。
- transaction_fact_seed_schema.yaml：定义交易事实种子。
- market_structure_fact_seed_schema.yaml：定义 K 线和成交基础事实，不得判断场景。
- source_reconciliation_record_schema.yaml：定义多源对账，不允许静默覆盖冲突。
- data_quality_record_schema.yaml：定义 completeness、freshness、consistency、traceability、source reliability、replayability、normalization score。
- data_freshness_policy.yaml：定义 quote、liquidity、wallet rows、holder snapshot、security scan、kline、legacy reference 的新鲜度规则。
- data_gap_policy.yaml：定义 blocking / critical / high / medium / low gap。
- data_conflict_policy.yaml：定义 price、market cap、liquidity、wallet holdings、holder snapshot 等冲突处理。
- p02_hard_negative_rules.yaml：定义无 P01 handoff、无 token 主键、无 raw、所有主源失败、静默覆盖冲突、P02 越权、自动实盘、无 trace 标准化等阻断规则。
- p02_state_machine.yaml：定义 P02 全状态机。
- p02_trace_requirements.yaml：定义 raw trace、field trace、contract trace、state trace、handoff trace。
- p03_data_request_packet_contract.yaml：定义 P02 给 P03 的钱包实体数据请求包。
- p02_to_p03_handoff_contract.yaml：定义 P02_TO_P03 handoff packet。
- p02_acceptance_criteria.md：定义 P02_READY、P02_READY_WITH_GAPS、P02_REJECTED、P02_BLOCKED。
- p02_storage_constitution.md：定义系统文件与运行数据目录。
- p02_test_matrix.yaml：定义至少 12 个测试场景。
- p02_report_model.yaml：定义 P02 人类可读报告。
- p02_review_checklist.md：定义审计清单。
- her_p02_execution_protocol.md：定义 HER 执行 P02 的步骤和禁止事项。

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. P02_READY / P02_READY_WITH_GAPS / P02_REJECTED / P02_BLOCKED 判断
4. raw_data_manifest 摘要
5. normalized_fact_package 摘要
6. token_fact_record 摘要
7. pair_pool_fact_record 摘要
8. market_fact_record 摘要
9. security_fact_record 摘要
10. wallet_fact_seed_record 摘要
11. source_reconciliation 摘要
12. data_quality_record 摘要
13. p03_data_request_packet 摘要
14. p02_to_p03_handoff_packet 摘要
15. P02 阻断规则摘要
16. P02 测试矩阵摘要
17. 当前缺口清单
18. 是否达到轻量机构级 P02 v3.0

最终验收标准：
只有当 P02 具备 raw_data_manifest、source_pull_record、source_data_fact_package、token_fact_record、pair_pool_fact_record、market_fact_record、security_fact_record、wallet_fact_seed_record、holder_snapshot_fact、transaction_fact_seed、market_structure_fact_seed、source_reconciliation_record、data_quality_record、freshness_policy、gap_policy、conflict_policy、hard_negative_rules、state_machine、trace_requirements、P03 data request、P02 handoff contract、acceptance criteria、storage constitution、test matrix、report model、HER execution protocol，并且 P02 不能输出证据、钱包角色、筹码判断、场景判断、策略准入、paper runtime 或 live execution 时，才允许标记为 P02_READY。
```

---

# 31. 当前是否达到专业化标准

## 判断

这一版 P02 才符合：

```text
专业化
轻量机构水准
一次性把阶段应有数据补全
不是最小版本
不是数据采集脚本
```

P02 被明确升级为：

```text
数据事实生产控制器
raw 数据保管层
normalized fact 标准化层
多源对账层
质量 / 新鲜度 / 缺口 / 冲突治理层
P03 钱包实体层的事实输入层
```

---

# 32. 本版补齐的关键能力

|能力|是否补齐|
|---|---|
|Raw Data Manifest|已补齐|
|Source Pull Record|已补齐|
|Source Data Fact Package|已补齐|
|Token Fact Record|已补齐|
|Pair / Pool Fact Record|已补齐|
|Market Fact Record|已补齐|
|Security Fact Record|已补齐|
|Wallet Fact Seed|已补齐|
|Holder Snapshot Fact|已补齐|
|Transaction Fact Seed|已补齐|
|Market Structure Fact Seed|已补齐|
|Source Reconciliation|已补齐|
|Data Quality|已补齐|
|Freshness Policy|已补齐|
|Gap Policy|已补齐|
|Conflict Policy|已补齐|
|P03 Data Request|已补齐|
|Handoff Contract|已补齐|
|Test Matrix|已补齐|
|Report Model|已补齐|
|HER Execution Protocol|已补齐|

---

# 33. 尚未解决问题

|问题|当前状态|后续处理|
|---|---|---|
|GMGN / OKX 真实字段名未完全对齐|P02 已定义需求|Tool Binding 阶段做 field mapping|
|数据源调用器未代码化|当前是控制器设计|Runner / Tool Binding 阶段实现|
|source reconciliation 阈值未回测|已定义模型|Review / Upgrade 校准|
|data quality 权重未验证|当前为初版|P09 / P10 校准|
|legacy runtime 数据未扫描|已定义路径|legacy mapping 工程任务|
|wallet_fact_seed 是否足够 P03|P03 展开时校验|下一阶段处理|
|security fact 不能替代 P08|已明确|P08 必须重新检查|
|P02 handoff 未联调|需要 P03|下一阶段展开 P03|

---

# 本次认知升级点

1. **P02 的本质是数据事实生产控制器，不是数据采集脚本。**
    
2. **raw 与 normalized 必须分离。**  
    raw 保管可审计，normalized 才能给下游使用。
    
3. **P02 必须做多源对账。**  
    GMGN、OKX、链上、K 线、holder snapshot 之间的冲突不能静默覆盖。
    
4. **P02 必须输出 P03 Data Request Packet。**  
    P03 Wallet Entity Controller 需要知道钱包实体归并要读什么、缺什么、哪些只能弱使用。
    
5. **P02 的安全事实不是执行安全通过。**  
    最终执行风险必须在 P08 重新判断。
    
6. **P02 的 wallet_fact_seed 不是钱包角色判断。**  
    钱包角色、同源组、主导侧结构都属于 P03 之后。
    
7. **P02 可以 READY_WITH_GAPS。**  
    因为它的职责是尽量生产事实并清楚传递缺口，而不是强行补全所有字段。
    
8. **P02 只能交接给 P03。**  
    任何跳过 P03-P06 直接进入策略或 runtime 的路径都必须阻断。