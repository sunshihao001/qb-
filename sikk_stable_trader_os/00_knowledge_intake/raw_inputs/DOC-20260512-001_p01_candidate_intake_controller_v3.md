。
 **P01 Candidate Intake Controller 专业版 v3.0**。

---

# P01 Candidate Intake Controller 专业版 v3.0

## 1. 阶段总定义

```text
P01 Candidate Intake Controller 是 SIKK Stable Trader OS 的候选主数据建档控制器。

它负责把所有进入系统的 token 候选，从“来源杂乱、身份不完整、上下文不清、可能重复、可能过期、可能来自 legacy 或 replay 的原始输入”，转换成“可追踪、可去重、可验收、可交接、可请求下游数据补全的标准 Candidate Master Record”。

P01 不判断机会。
P01 不判断钱包。
P01 不判断筹码。
P01 不判断证据。
P01 不判断场景。
P01 不判断策略。
P01 不允许进入 paper runtime。
P01 不允许任何 live execution。
```

P01 的专业目标不是“找到好币”，而是：

```text
建立一个干净、可治理、可追踪、可交接的候选入口。
```

---

# 2. P01 的专业化目标

## 2.1 阶段目标

P01 必须一次性解决 10 个问题：

|编号|问题|P01 必须输出|
|---|---|---|
|1|这个候选是谁？|`candidate_master_record`|
|2|从哪里来？|`candidate_source_event`|
|3|什么时候进入系统？|`intake_time_context`|
|4|是否重复？|`dedup_resolution_record`|
|5|身份是否完整？|`identity_resolution_record`|
|6|来源是否可信？|`source_quality_record`|
|7|是否存在阻断问题？|`p01_hard_negative_result`|
|8|哪些字段缺失？|`p01_gap_report`|
|9|下游 P02 需要补什么数据？|`p02_data_request_packet`|
|10|是否可交接？|`p01_to_p02_handoff_packet`|

---

# 3. P01 的角色模型

P01 应该按 6 个专业角色来设计，而不是只按“候选导入器”来设计。

|角色|负责问题|输出|
|---|---|---|
|情报接收官|候选从哪里来|source event|
|主数据治理官|token 身份是否唯一|candidate master|
|去重归并官|是否重复发现|dedup record|
|数据质量官|字段是否完整、可用|quality score|
|审计官|是否可追踪、可回放|trace / audit|
|交接官|下游应该读什么、补什么|handoff / data request|

---

# 4. P01 底层方法论

## 4.1 主数据管理原则

P01 的核心资产是：

```text
Candidate Master Record
```

不是临时列表。

一个 token 在系统中只能有一个主候选对象：

```text
chain + token_address → candidate_id
```

所有重复来源都必须追加为 source event，而不是新建候选。

---

## 4.2 证据保管链原则

候选从进入系统开始就必须可追踪：

```text
raw_source_input
  ↓
source_event
  ↓
normalized_candidate
  ↓
candidate_master_record
  ↓
intake_status
  ↓
P01 acceptance
  ↓
P01 handoff
  ↓
P02 data request
```

任何无来源、无 trace、无 candidate_id 的候选都不能进入 P02。

---

## 4.3 零信任输入原则

所有候选来源默认不可信，必须先验证身份。

```text
GMGN 热门榜 ≠ 好机会
Smart Money 来源 ≠ 结构支持
KOL 提及 ≠ 可交易
人工输入 ≠ 自动可信
legacy runtime ≠ 新标准
replay sample ≠ 实时样本
```

P01 只确认候选身份与来源上下文，不对交易质量背书。

---

## 4.4 阶段权限隔离原则

P01 只能做：

```text
接收
建档
去重
标源
标缺口
生成下游数据请求
交接给 P02
```

P01 不能做：

```text
证据生成
场景识别
策略准入
纸面交易
自动实盘
```

---

# 5. P01 必须建立的核心对象

## 5.1 对象总表

|对象|作用|
|---|---|
|`Candidate Raw Input`|原始候选输入|
|`Candidate Source Event`|每次候选被发现或输入的来源事件|
|`Candidate Master Record`|候选主记录|
|`Token Identity Record`|token 身份解析|
|`Pool Identity Record`|pool / pair 解析|
|`Discovery Context`|发现时上下文|
|`Intake Time Context`|时间上下文|
|`Dedup Resolution Record`|去重归并结果|
|`Source Quality Record`|来源质量评估|
|`Candidate Risk Precheck`|入口层硬阻断检查|
|`Candidate Gap Record`|缺口登记|
|`P02 Data Request Packet`|下游数据请求包|
|`P01 Acceptance Packet`|P01 验收结果|
|`P01 Handoff Packet`|P01 → P02 交接包|
|`P01 Audit Record`|审计记录|

---

# 6. Candidate Master Record

这是 P01 最核心的数据结构。

```yaml
candidate_master_record:
  candidate_id: string
  candidate_version: string
  candidate_status:
    - INTAKE_RECEIVED
    - IDENTITY_PENDING
    - IDENTITY_VERIFIED
    - DUPLICATE_MERGED
    - READY_FOR_P02
    - READY_FOR_P02_WITH_GAPS
    - REJECTED
    - BLOCKED

  token_identity:
    chain: string
    token_address: string
    token_address_normalized: string
    token_address_valid: boolean
    token_symbol: string | null
    token_name: string | null
    token_decimals: integer | null
    token_standard: string | null

  pool_identity:
    pair_address: string | null
    pool_address: string | null
    dex_name: string | null
    quote_token: string | null
    base_token: string | null
    pool_identity_status:
      - POOL_CONFIRMED
      - POOL_MISSING
      - MULTI_POOL_DETECTED
      - POOL_CONFLICTED
      - UNKNOWN

  source_summary:
    first_source_type: string
    first_source_id: string
    first_seen_by_system_at: datetime
    latest_source_type: string
    latest_seen_at: datetime
    source_event_count: integer
    rediscovery_count: integer
    source_types_seen: list

  discovery_context:
    discovery_time: datetime
    discovery_market_cap_usd: number | null
    discovery_liquidity_usd: number | null
    discovery_price_usd: number | null
    discovery_holder_count: integer | null
    discovery_token_age_seconds: integer | null
    discovery_source_rank: integer | null
    discovery_reason: string | null

  intake_context:
    intake_run_id: string
    intake_batch_id: string | null
    intake_mode:
      - LIVE
      - MANUAL
      - REPLAY
      - LEGACY_IMPORT
      - TEST
    intake_priority:
      - HIGH
      - MEDIUM
      - LOW
      - WATCH_ONLY
    paper_only: true
    live_execution_allowed: false

  quality:
    identity_quality_status: string
    source_quality_status: string
    intake_quality_score: number
    required_fields_present: integer
    required_fields_missing: integer
    quality_limitations: list

  trace:
    candidate_trace_id: string
    source_trace_ids: list
    identity_trace_id: string
    dedup_trace_id: string | null
    state_trace_ids: list
    artifact_trace_ids: list

  downstream:
    allowed_next_controller:
      - P02_SOURCE_DATA_FACT_CONTROLLER
    forbidden_next_controller:
      - P03_WALLET_ENTITY_CONTROLLER
      - P04_CHIP_STRUCTURE_CONTROLLER
      - P05_EVIDENCE_CONTROLLER
      - P06_SCENARIO_RECOGNITION_CONTROLLER
      - P07_STRATEGY_GATE_CONTROLLER
      - PAPER_ONLY_RUNTIME
      - LIVE_EXECUTION

  gaps:
    blocking_gaps: list
    critical_gaps: list
    high_gaps: list
    medium_gaps: list
    low_gaps: list

  audit:
    created_at: datetime
    updated_at: datetime
    created_by_controller: P01_CANDIDATE_INTAKE_CONTROLLER
    last_update_reason: string
```

---

# 7. Candidate Source Event

P01 不能只存“来源类型”，必须记录每一次来源事件。

```yaml
candidate_source_event:
  source_event_id: string
  candidate_id: string
  event_time: datetime
  received_at: datetime

  source:
    source_type:
      - GMGN_TRENDING
      - GMGN_NEW_TOKEN
      - GMGN_SMART_MONEY
      - GMGN_KOL_SIGNAL
      - MANUAL_INPUT
      - TELEGRAM_COMMAND
      - LEGACY_RUNTIME
      - REPLAY_SAMPLE
      - WATCHLIST_IMPORT
      - EXTERNAL_CSV_IMPORT
      - SYSTEM_REDISCOVERY
    source_id: string
    source_name: string
    source_rank: integer | null
    source_url: string | null
    source_payload_path: string | null
    source_message_id: string | null
    operator_id: string | null

  raw_input:
    raw_token_address: string | null
    raw_chain: string | null
    raw_pair_address: string | null
    raw_pool_address: string | null
    raw_symbol: string | null
    raw_note: string | null

  source_reason:
    reason_type:
      - TRENDING
      - NEW_LAUNCH
      - SMART_MONEY_ACTIVITY
      - KOL_MENTION
      - MANUAL_WATCH
      - REPLAY_TEST
      - LEGACY_REFERENCE
      - UNKNOWN
    reason_text: string | null

  quality:
    source_reliability_score: number
    source_timeliness_score: number
    source_identity_completeness_score: number
    source_replayability_score: number
    source_traceability_score: number
    source_quality_status:
      - SOURCE_HIGH_CONFIDENCE
      - SOURCE_USABLE
      - SOURCE_USABLE_WITH_GAPS
      - SOURCE_LOW_CONFIDENCE
      - SOURCE_REJECTED

  trace:
    source_trace_id: string
    raw_input_trace_id: string | null

  downstream_usage:
    may_support_candidate_intake: boolean
    may_support_evidence: false
    may_support_strategy: false
```

---

# 8. Token Identity Resolution

P01 必须做身份解析，但不能做深度数据事实。

```yaml
token_identity_resolution:
  identity_resolution_id: string
  candidate_id: string

  input_identity:
    raw_chain: string | null
    raw_token_address: string | null
    raw_pair_address: string | null
    raw_pool_address: string | null

  normalized_identity:
    chain: string
    token_address_normalized: string
    pair_address_normalized: string | null
    pool_address_normalized: string | null

  validation:
    chain_supported: boolean
    token_address_format_valid: boolean
    token_address_checksum_valid: boolean | null
    pair_address_format_valid: boolean | null
    pool_address_format_valid: boolean | null

  identity_conflict:
    symbol_collision_detected: boolean
    same_symbol_different_address: boolean
    same_address_multiple_pools: boolean
    identity_conflict_status:
      - NO_CONFLICT
      - SYMBOL_COLLISION
      - MULTI_POOL
      - ADDRESS_CONFLICT
      - UNKNOWN

  result:
    identity_status:
      - IDENTITY_VERIFIED
      - IDENTITY_VERIFIED_WITH_GAPS
      - IDENTITY_CONFLICTED
      - IDENTITY_REJECTED
    reason: string

  trace:
    identity_trace_id: string
```

---

# 9. Discovery Context

发现上下文是后续判断“早不早、是否追高、是否退出流动性”的基础。

```yaml
discovery_context:
  candidate_id: string

  time:
    discovery_time: datetime
    first_seen_by_system_at: datetime
    source_observed_time: datetime | null
    ingestion_delay_seconds: integer | null

  market_snapshot_at_discovery:
    discovery_market_cap_usd: number | null
    discovery_liquidity_usd: number | null
    discovery_price_usd: number | null
    discovery_volume_5m_usd: number | null
    discovery_volume_1h_usd: number | null
    discovery_holder_count: integer | null
    discovery_token_age_seconds: integer | null

  source_position:
    source_rank: integer | null
    source_category: string | null
    source_signal_strength: string | null

  freshness:
    discovery_context_freshness:
      - FRESH
      - ACCEPTABLE
      - STALE
      - UNKNOWN
    freshness_reason: string

  gaps:
    missing_discovery_fields: list
    data_to_request_from_p02: list
```

---

# 10. Intake Time Context

P01 必须区分实时、回放、旧数据、人工输入。

```yaml
intake_time_context:
  candidate_id: string
  intake_mode:
    - LIVE
    - MANUAL
    - REPLAY
    - LEGACY_IMPORT
    - TEST

  system_time:
    received_at: datetime
    intake_started_at: datetime
    intake_completed_at: datetime | null

  candidate_time:
    token_launch_time: datetime | null
    discovery_time: datetime | null
    source_observed_time: datetime | null

  time_alignment:
    launch_to_discovery_seconds: integer | null
    discovery_to_intake_seconds: integer | null
    source_to_system_delay_seconds: integer | null

  time_risk_status:
    - TIME_CONTEXT_OK
    - DISCOVERY_TIME_MISSING
    - SOURCE_DELAY_HIGH
    - TOKEN_AGE_UNKNOWN
    - REPLAY_TIME_CONTEXT
    - LEGACY_TIME_CONTEXT

  downstream_note:
    p02_must_refresh_market_data: boolean
    p02_must_establish_launch_time: boolean
```

---

# 11. Dedup Resolution Record

专业系统必须避免同一 token 重复进入后续阶段。

```yaml
dedup_resolution_record:
  dedup_id: string
  candidate_id: string

  primary_key:
    chain: string
    token_address: string

  secondary_keys:
    pair_address: string | null
    pool_address: string | null
    token_symbol: string | null

  dedup_result:
    dedup_status:
      - NEW_CANDIDATE
      - EXACT_DUPLICATE_MERGED
      - REDISCOVERY_MERGED
      - MULTI_POOL_ATTACHED
      - LEGACY_MATCH_ATTACHED
      - SYMBOL_COLLISION_FLAGGED
      - IDENTITY_CONFLICT_REJECTED

  matched_existing_candidate_id: string | null
  source_events_merged: list
  duplicate_reason: string | null

  merge_policy:
    preserve_first_seen_time: true
    append_new_source_event: true
    do_not_overwrite_discovery_market_cap: true
    attach_latest_context_separately: true

  trace:
    dedup_trace_id: string
```

---

# 12. Candidate Quality Model

P01 需要候选建档质量评分，而不是交易评分。

```yaml
candidate_intake_quality_model:
  dimensions:
    identity_completeness:
      weight: 0.25
      checks:
        - token_address_present
        - chain_present
        - token_address_valid
        - pool_or_pair_present_or_requested

    source_traceability:
      weight: 0.20
      checks:
        - source_type_present
        - source_id_present
        - source_trace_id_present
        - raw_source_payload_available

    discovery_context_quality:
      weight: 0.20
      checks:
        - discovery_time_present
        - discovery_market_cap_present
        - discovery_liquidity_present
        - token_age_present

    dedup_integrity:
      weight: 0.15
      checks:
        - duplicate_check_completed
        - candidate_id_stable
        - rediscovery_attached_not_recreated

    downstream_readiness:
      weight: 0.20
      checks:
        - p02_data_request_generated
        - gaps_registered
        - limitation_tags_attached
        - handoff_packet_ready

  quality_status:
    - INTAKE_HIGH_CONFIDENCE
    - INTAKE_USABLE
    - INTAKE_USABLE_WITH_GAPS
    - INTAKE_LOW_CONFIDENCE
    - INTAKE_REJECTED
```

---

# 13. P01 Gap Policy

P01 缺口必须分级，并决定是否允许进入 P02。

```yaml
p01_gap_policy:
  BLOCKING_GAP:
    result: P01_BLOCKED
    examples:
      - live_execution_requested
      - unsupported_chain
      - no_handoff_permission
      - no_trace_allowed
      - handoff_plane_bypassed

  CRITICAL_GAP:
    result: P01_REJECTED
    examples:
      - token_address_missing
      - token_address_invalid
      - source_type_missing
      - candidate_id_generation_failed
      - candidate_identity_conflict_unresolved

  HIGH_GAP:
    result: P01_READY_WITH_GAPS
    downstream_permission: P02_ONLY
    examples:
      - pair_address_missing
      - pool_address_missing
      - discovery_time_uncertain
      - raw_source_payload_missing
      - source_trace_partial

  MEDIUM_GAP:
    result: P01_READY_WITH_GAPS
    downstream_permission: P02_ONLY
    examples:
      - discovery_market_cap_missing
      - discovery_liquidity_missing
      - discovery_holder_count_missing
      - token_age_missing
      - source_rank_missing

  LOW_GAP:
    result: P01_READY_WITH_GAPS
    downstream_permission: P02_ONLY
    examples:
      - token_symbol_missing
      - token_name_missing
      - source_reason_missing
```

---

# 14. P02 Data Request Packet

这是上一版严重缺失的部分。P01 不只是交接候选，还必须告诉 P02 要补什么数据。

```yaml
p02_data_request_packet:
  packet_id: string
  from_controller: P01_CANDIDATE_INTAKE_CONTROLLER
  to_controller: P02_SOURCE_DATA_FACT_CONTROLLER
  generated_at: datetime

  candidate_scope:
    candidate_ids: list
    token_addresses: list
    chain: string

  required_data_requests:
    token_identity:
      - token_symbol
      - token_name
      - token_decimals
      - pair_address
      - pool_address
      - deployer_address
      - creator_address
      - launch_time

    market_discovery_context:
      - current_market_cap_usd
      - discovery_market_cap_usd_if_available
      - liquidity_usd
      - price_usd
      - holder_count
      - token_age_seconds

    security_precheck:
      - mint_authority_status
      - freeze_authority_status
      - blacklist_risk
      - transfer_restriction_status
      - honeypot_risk

    source_reconciliation:
      - gmgn_token_profile
      - gmgn_pair_profile
      - okx_quote_if_available
      - chain_raw_identity_check

  priority:
    high_priority:
      - token_address
      - chain
      - pair_address
      - pool_address
      - current_market_cap_usd
      - liquidity_usd
      - security_precheck

    medium_priority:
      - holder_count
      - token_age_seconds
      - deployer_address

    low_priority:
      - token_symbol
      - token_name

  limitations_from_p01:
    - CANDIDATE_ONLY
    - NO_EVIDENCE
    - NO_SCENARIO
    - NO_STRATEGY_GATE
    - LIVE_EXECUTION_FORBIDDEN

  gaps_to_resolve:
    gap_ids: list
    missing_fields_by_candidate: object
```

---

# 15. P01 状态机专业版

```yaml
p01_candidate_intake_state_machine:
  states:
    - P01_UNINITIALIZED
    - P01_CONTEXT_LOADED
    - P01_HANDOFF_READ
    - P01_INPUT_RECEIVED
    - P01_SOURCE_REGISTERED
    - P01_RAW_INPUT_SAVED
    - P01_IDENTITY_NORMALIZED
    - P01_IDENTITY_VERIFIED
    - P01_IDENTITY_CONFLICTED
    - P01_DEDUP_RUNNING
    - P01_DEDUP_COMPLETED
    - P01_DISCOVERY_CONTEXT_BUILT
    - P01_GAP_ANALYZED
    - P01_QUALITY_SCORED
    - P01_P02_DATA_REQUEST_BUILT
    - P01_READY_FOR_ACCEPTANCE
    - P01_ACCEPTANCE_READY
    - P01_READY_FOR_P02_HANDOFF
    - P01_READY_WITH_GAPS
    - P01_REJECTED
    - P01_BLOCKED

  transitions:
    - from: P01_INPUT_RECEIVED
      to: P01_SOURCE_REGISTERED
      condition: source_type_present == true

    - from: P01_SOURCE_REGISTERED
      to: P01_RAW_INPUT_SAVED
      condition: raw_input_stored_or_reference_registered == true

    - from: P01_RAW_INPUT_SAVED
      to: P01_IDENTITY_NORMALIZED
      condition: token_address_present == true

    - from: P01_IDENTITY_NORMALIZED
      to: P01_IDENTITY_VERIFIED
      condition: token_address_valid == true and chain_supported == true

    - from: P01_IDENTITY_NORMALIZED
      to: P01_IDENTITY_CONFLICTED
      condition: identity_conflict_detected == true

    - from: P01_IDENTITY_VERIFIED
      to: P01_DEDUP_RUNNING
      condition: candidate_id_generated == true

    - from: P01_DEDUP_RUNNING
      to: P01_DEDUP_COMPLETED
      condition: dedup_resolution_record_created == true

    - from: P01_DEDUP_COMPLETED
      to: P01_DISCOVERY_CONTEXT_BUILT
      condition: discovery_context_record_created == true

    - from: P01_DISCOVERY_CONTEXT_BUILT
      to: P01_GAP_ANALYZED
      condition: gap_report_created == true

    - from: P01_GAP_ANALYZED
      to: P01_QUALITY_SCORED
      condition: candidate_quality_score_created == true

    - from: P01_QUALITY_SCORED
      to: P01_P02_DATA_REQUEST_BUILT
      condition: p02_data_request_packet_created == true

    - from: P01_P02_DATA_REQUEST_BUILT
      to: P01_READY_FOR_ACCEPTANCE
      condition: p01_output_contract_ready == true

    - from: P01_READY_FOR_ACCEPTANCE
      to: P01_ACCEPTANCE_READY
      condition: acceptance_status in [ACCEPTANCE_READY, ACCEPTANCE_READY_WITH_GAPS]

    - from: P01_ACCEPTANCE_READY
      to: P01_READY_FOR_P02_HANDOFF
      condition: p01_to_p02_handoff_packet_created == true
```

---

# 16. P01 阻断规则专业版

```yaml
p01_hard_negative_rules:
  - rule_id: P01_BLOCK_001
    name: token_address 缺失
    condition: token_address is null
    result: P01_REJECTED
    reason: 无法建立候选主键

  - rule_id: P01_BLOCK_002
    name: chain 缺失或不支持
    condition: chain is null or chain not in supported_chains
    result: P01_BLOCKED
    reason: 系统无法处理该候选

  - rule_id: P01_BLOCK_003
    name: 来源不可追踪
    condition: source_type is null and source_trace_id is null
    result: P01_REJECTED
    reason: 无来源链无法审计

  - rule_id: P01_BLOCK_004
    name: 候选身份冲突
    condition: same_candidate_id_maps_to_multiple_token_addresses
    result: P01_REJECTED
    reason: 主键冲突不能进入 P02

  - rule_id: P01_BLOCK_005
    name: 跳过 P02 请求
    condition: requested_next_controller != P02_SOURCE_DATA_FACT_CONTROLLER
    result: P01_BLOCKED
    reason: P01 只能交接给 P02

  - rule_id: P01_BLOCK_006
    name: 输出交易判断
    condition: output_contains in [buy_signal, paper_ready, strategy_gate_decision, scenario_claim]
    result: P01_BLOCKED
    reason: P01 越权

  - rule_id: P01_BLOCK_007
    name: 自动实盘路径
    condition: live_execution_requested == true or live_execution_allowed == true
    result: P01_BLOCKED
    reason: 当前系统保持 paper-only

  - rule_id: P01_BLOCK_008
    name: 未经 Handoff 输入
    condition: upstream_handoff_packet_missing == true
    result: P01_BLOCKED
    reason: P01 不能绕过 Handoff Plane 启动

  - rule_id: P01_BLOCK_009
    name: 未经 Acceptance
    condition: acceptance_result_packet_missing == true
    result: P01_BLOCKED
    reason: P01 必须受 Acceptance Plane 管控

  - rule_id: P01_BLOCK_010
    name: 无 trace 建档
    condition: candidate_trace_id is null
    result: P01_BLOCKED
    reason: 无 trace 不能进入主候选注册表
```

---

# 17. P01 输出文件体系

建议目录：

```text
/root/sikk-gmgn/system/phase_controllers/p01_candidate_intake_controller/
```

系统文件：

```text
p01_candidate_intake_controller.yaml
p01_candidate_intake_context.md
p01_input_contract.yaml
p01_output_contract.yaml
candidate_master_record_schema.yaml
candidate_source_event_schema.yaml
token_identity_resolution_schema.yaml
discovery_context_schema.yaml
intake_time_context_schema.yaml
dedup_resolution_schema.yaml
candidate_source_registry.yaml
candidate_source_quality_model.yaml
candidate_intake_quality_model.yaml
candidate_intake_gap_policy.yaml
candidate_intake_state_machine.yaml
candidate_intake_hard_negative_rules.yaml
candidate_intake_trace_requirements.yaml
p02_data_request_packet_contract.yaml
candidate_intake_handoff_contract.yaml
candidate_intake_acceptance_criteria.md
candidate_intake_storage_constitution.md
candidate_intake_test_matrix.yaml
candidate_intake_report_model.yaml
candidate_intake_review_checklist.md
her_p01_execution_protocol.md
```

运行数据目录：

```text
/root/sikk-gmgn/data/phase_controllers/p01_candidate_intake/
  source_inbox/
  raw_candidate_inputs/
  source_events/
  normalized_candidates/
  candidate_master/
  token_identity/
  pool_identity/
  discovery_context/
  intake_time_context/
  dedup_resolution/
  duplicate_index/
  source_quality/
  intake_quality/
  gap_reports/
  p02_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/
```

---

# 18. P01 测试矩阵

专业系统必须定义测试样例，不只是定义字段。

```yaml
candidate_intake_test_matrix:
  - test_id: P01_TEST_001
    name: 正常 GMGN 候选输入
    input: token_address + chain + source_type
    expected_status: READY_FOR_P02

  - test_id: P01_TEST_002
    name: 缺 token_address
    input: chain + source_type only
    expected_status: P01_REJECTED

  - test_id: P01_TEST_003
    name: 重复 token 再次发现
    input: same chain + same token_address + new source
    expected_status: DUPLICATE_MERGED

  - test_id: P01_TEST_004
    name: 同 symbol 不同 token
    input: same symbol + different token_address
    expected_status: SYMBOL_COLLISION_FLAGGED

  - test_id: P01_TEST_005
    name: legacy runtime 导入
    input: legacy token record
    expected_status: READY_WITH_GAPS
    required_limitation: LEGACY_REFERENCE_ONLY

  - test_id: P01_TEST_006
    name: replay sample 输入
    input: replay candidate
    expected_status: READY_WITH_GAPS
    required_limitation: REPLAY_CONTEXT

  - test_id: P01_TEST_007
    name: 请求直接进入策略层
    input: token + requested_next_stage=P07
    expected_status: P01_BLOCKED

  - test_id: P01_TEST_008
    name: 自动实盘请求
    input: token + live_execution_requested=true
    expected_status: P01_BLOCKED

  - test_id: P01_TEST_009
    name: 缺 discovery market cap
    input: token + source but no market cap
    expected_status: READY_WITH_GAPS
    required_p02_request: current_market_cap_usd

  - test_id: P01_TEST_010
    name: 无 trace 输入
    input: token but no trace
    expected_status: P01_BLOCKED
```

---

# 19. P01 报告模型

```yaml
candidate_intake_report:
  report_id: string
  generated_at: datetime
  controller_id: P01_CANDIDATE_INTAKE_CONTROLLER

  summary:
    total_inputs_received: integer
    total_candidates_created: integer
    total_duplicates_merged: integer
    total_ready_for_p02: integer
    total_ready_with_gaps: integer
    total_rejected: integer
    total_blocked: integer

  source_breakdown:
    by_source_type: object
    source_quality_distribution: object

  identity_breakdown:
    verified_count: integer
    verified_with_gaps_count: integer
    conflicted_count: integer
    rejected_count: integer

  gap_summary:
    blocking_gaps: list
    critical_gaps: list
    high_gaps: list
    medium_gaps: list
    low_gaps: list

  p02_request_summary:
    total_data_requests: integer
    most_common_missing_fields: list
    high_priority_requests: list

  compliance:
    p01_forbidden_outputs_detected: boolean
    live_execution_path_detected: boolean
    all_candidates_have_trace: boolean
    handoff_ready: boolean

  next_stage:
    allowed_next_controller: P02_SOURCE_DATA_FACT_CONTROLLER
    handoff_packet_path: string
```

---

# 20. P01 Handoff Contract 专业版

```yaml
p01_to_p02_handoff_packet:
  packet_id: string
  packet_type: P01_TO_P02_CANDIDATE_INTAKE_HANDOFF
  generated_at: datetime

  route:
    from_controller: P01_CANDIDATE_INTAKE_CONTROLLER
    to_controller: P02_SOURCE_DATA_FACT_CONTROLLER

  upstream_control:
    acceptance_result_packet_id: string
    trace_handoff_packet_id: string
    handoff_trace_id: string

  candidate_registry:
    candidate_master_index_path: string
    candidate_registry_json_path: string
    candidate_registry_csv_path: string
    candidate_count_total: integer
    candidate_count_ready_for_p02: integer
    candidate_count_ready_with_gaps: integer
    candidate_count_rejected: integer
    candidate_count_blocked: integer

  candidate_objects:
    candidate_master_records_path: string
    source_events_path: string
    identity_resolution_path: string
    discovery_context_path: string
    dedup_resolution_path: string

  p02_data_request:
    p02_data_request_packet_path: string
    high_priority_requests: list
    missing_fields_by_candidate: object

  quality_summary:
    intake_quality_status_distribution: object
    source_quality_status_distribution: object
    identity_quality_status_distribution: object

  gap_transfer:
    propagated_gap_report_path: string
    blocking_gaps: list
    non_blocking_gaps: list
    limitations:
      - CANDIDATE_ONLY
      - NO_EVIDENCE
      - NO_SCENARIO
      - NO_STRATEGY_GATE
      - NO_RUNTIME
      - LIVE_EXECUTION_FORBIDDEN

  downstream_permission:
    allowed:
      - P02_SOURCE_DATA_FACT_CONTROLLER
    forbidden:
      - P03_WALLET_ENTITY_CONTROLLER
      - P04_CHIP_STRUCTURE_CONTROLLER
      - P05_EVIDENCE_CONTROLLER
      - P06_SCENARIO_RECOGNITION_CONTROLLER
      - P07_STRATEGY_GATE_CONTROLLER
      - PAPER_ONLY_RUNTIME
      - LIVE_EXECUTION

  read_instruction:
    p02_must_read_first:
      - p01_to_p02_handoff_packet
      - candidate_master_records
      - p02_data_request_packet
      - gap_report
      - limitation_tags

  audit:
    report_path: string
    audit_log_path: string
```

---

# 21. HER P01 执行协议专业版

```text
HER 执行 P01 时必须按以下顺序：

1. 读取 professional_build_order.md
2. 读取 phase_controller_index.yaml
3. 读取 Handoff Plane 输出的 handoff_packet
4. 读取 Acceptance Plane 输出的 acceptance_result_packet
5. 读取 Trace Plane 输出的 trace_handoff_packet
6. 读取 P01 controller context
7. 校验 P01 输入合约
8. 接收 candidate raw input
9. 保存 raw_candidate_input 或 source reference
10. 创建 candidate_source_event
11. 规范化 token identity
12. 校验 chain 和 token_address
13. 生成 candidate_id
14. 执行 dedup resolution
15. 建立 candidate_master_record
16. 建立 discovery_context
17. 建立 intake_time_context
18. 计算 source_quality
19. 计算 intake_quality
20. 执行 hard negative rules
21. 建立 p01_gap_report
22. 生成 p02_data_request_packet
23. 写入 P01 trace
24. 生成 candidate_registry
25. 生成 candidate_intake_report
26. 生成 p01_to_p02_handoff_packet
27. 执行 P01 acceptance
28. 只允许 handoff 给 P02
```

禁止：

```text
1. 不允许无 Handoff 启动 P01
2. 不允许无 Acceptance 启动 P01
3. 不允许无 Trace 建立 candidate
4. 不允许无 token_address 建档
5. 不允许无 source_context 建档
6. 不允许 P01 输出 evidence
7. 不允许 P01 输出 scenario
8. 不允许 P01 输出 strategy gate
9. 不允许 P01 输出 paper ready
10. 不允许 P01 进入 runtime
11. 不允许任何 live execution
```

---

# 22. 给 HER 的专业化任务书

```text
任务名称：重建 P01 Candidate Intake Controller 专业版 v3.0

目标：
在 /root/sikk-gmgn/system/phase_controllers/p01_candidate_intake_controller/ 下重建 P01 Candidate Intake Controller。该控制器不是候选发现脚本，也不是简单 token 列表，而是候选主数据建档控制器，负责将所有进入系统的 token 候选转换为可追踪、可去重、可验收、可交接、可请求 P02 数据补全的 Candidate Master Record。

核心原则：
1. P01 只负责候选接收、来源登记、身份解析、去重归并、基础上下文、缺口登记、P02 数据请求和 P01→P02 handoff。
2. P01 不做钱包结构分析。
3. P01 不做筹码结构分析。
4. P01 不生成证据。
5. P01 不识别场景。
6. P01 不做策略准入。
7. P01 不进入 paper runtime。
8. P01 不允许 live execution。
9. 每个候选必须有 candidate_id、source_event、candidate_master_record、intake_status、trace。
10. P01 必须生成 p02_data_request_packet，告诉 P02 需要补哪些数据。

需要创建系统目录：
/root/sikk-gmgn/system/phase_controllers/p01_candidate_intake_controller/

需要创建系统文件：
1. p01_candidate_intake_controller.yaml
2. p01_candidate_intake_context.md
3. p01_input_contract.yaml
4. p01_output_contract.yaml
5. candidate_master_record_schema.yaml
6. candidate_source_event_schema.yaml
7. token_identity_resolution_schema.yaml
8. pool_identity_resolution_schema.yaml
9. discovery_context_schema.yaml
10. intake_time_context_schema.yaml
11. dedup_resolution_schema.yaml
12. candidate_source_registry.yaml
13. candidate_source_quality_model.yaml
14. candidate_intake_quality_model.yaml
15. candidate_intake_gap_policy.yaml
16. candidate_intake_state_machine.yaml
17. candidate_intake_hard_negative_rules.yaml
18. candidate_intake_trace_requirements.yaml
19. p02_data_request_packet_contract.yaml
20. candidate_intake_handoff_contract.yaml
21. candidate_intake_acceptance_criteria.md
22. candidate_intake_storage_constitution.md
23. candidate_intake_test_matrix.yaml
24. candidate_intake_report_model.yaml
25. candidate_intake_review_checklist.md
26. her_p01_execution_protocol.md

需要创建运行数据目录：
/root/sikk-gmgn/data/phase_controllers/p01_candidate_intake/
  source_inbox/
  raw_candidate_inputs/
  source_events/
  normalized_candidates/
  candidate_master/
  token_identity/
  pool_identity/
  discovery_context/
  intake_time_context/
  dedup_resolution/
  duplicate_index/
  source_quality/
  intake_quality/
  gap_reports/
  p02_data_requests/
  rejected_candidates/
  blocked_candidates/
  trace/
  acceptance/
  handoff/
  reports/
  audit/

每个文件要求：
- p01_candidate_intake_controller.yaml：定义控制器身份、职责、权限、上下游、状态码、禁止事项。
- p01_candidate_intake_context.md：写成 HER 执行前必须读取的 P01 上下文。
- p01_input_contract.yaml：定义输入来源、输入格式、最低身份要求、缺失处理。
- p01_output_contract.yaml：定义 candidate registry、candidate master、gap report、P02 data request、handoff packet 输出。
- candidate_master_record_schema.yaml：定义标准候选主记录。
- candidate_source_event_schema.yaml：定义每次来源事件。
- token_identity_resolution_schema.yaml：定义 token identity 解析与校验。
- pool_identity_resolution_schema.yaml：定义 pool / pair 身份解析。
- discovery_context_schema.yaml：定义发现时上下文。
- intake_time_context_schema.yaml：定义实时、人工、replay、legacy、test 的时间上下文。
- dedup_resolution_schema.yaml：定义去重、重复发现、legacy match、多池归并、symbol collision。
- candidate_source_registry.yaml：定义 GMGN_TRENDING、GMGN_NEW_TOKEN、GMGN_SMART_MONEY、GMGN_KOL_SIGNAL、MANUAL_INPUT、TELEGRAM_COMMAND、LEGACY_RUNTIME、REPLAY_SAMPLE、WATCHLIST_IMPORT、EXTERNAL_CSV_IMPORT、SYSTEM_REDISCOVERY。
- candidate_source_quality_model.yaml：定义来源质量评分。
- candidate_intake_quality_model.yaml：定义候选建档质量评分。
- candidate_intake_gap_policy.yaml：定义 blocking / critical / high / medium / low gap。
- candidate_intake_state_machine.yaml：定义 P01 全状态机。
- candidate_intake_hard_negative_rules.yaml：定义 token 缺失、chain 不支持、来源不可追踪、身份冲突、跳过 P02、输出交易判断、自动实盘、无 handoff、无 acceptance、无 trace 等阻断。
- candidate_intake_trace_requirements.yaml：定义 candidate_trace_id、source_trace_id、identity_trace_id、dedup_trace_id、state_trace_id、handoff_trace_id。
- p02_data_request_packet_contract.yaml：定义 P01 给 P02 的数据请求包。
- candidate_intake_handoff_contract.yaml：定义 P01_TO_P02 handoff packet。
- candidate_intake_acceptance_criteria.md：定义 P01_READY、P01_READY_WITH_GAPS、P01_REJECTED、P01_BLOCKED。
- candidate_intake_storage_constitution.md：定义系统文件和运行数据目录。
- candidate_intake_test_matrix.yaml：定义至少 10 个测试场景，包括正常输入、缺 token、重复发现、symbol collision、legacy、replay、跳过 P02、自动实盘、缺 discovery market cap、无 trace。
- candidate_intake_report_model.yaml：定义 P01 人类可读报告。
- candidate_intake_review_checklist.md：定义审计清单。
- her_p01_execution_protocol.md：定义 HER 执行 P01 的步骤和禁止事项。

验收输出：
1. 文件创建清单
2. 每个文件核心摘要
3. P01_READY / P01_READY_WITH_GAPS / P01_REJECTED / P01_BLOCKED 判断
4. Candidate Master Record 字段摘要
5. Candidate Source Event 字段摘要
6. Token Identity Resolution 摘要
7. Dedup Policy 摘要
8. Source Quality Model 摘要
9. P02 Data Request Packet 摘要
10. P01 Handoff Packet 摘要
11. P01 阻断规则摘要
12. P01 测试矩阵摘要
13. 当前缺口清单
14. 是否达到轻量机构级 P01 v3.0

最终验收标准：
只有当 P01 具备 candidate master、source event、identity resolution、pool identity、discovery context、intake time context、dedup resolution、source quality、intake quality、gap policy、state machine、hard negative rules、trace requirements、P02 data request、handoff contract、acceptance criteria、storage constitution、test matrix、report model、HER execution protocol，并且 P01 不能输出证据、场景、策略、paper runtime 或 live execution 时，才允许标记为 P01_READY。
```

---

# 23. 当前是否达到专业化标准

## 判断

这一版才符合你要求的：

```text
专业化
轻量机构水准
一次性把 P01 阶段应有数据补全
不是最小版本
不是表面控制器
```

它把 P01 从：

```text
候选导入模块
```

提升为：

```text
候选主数据治理控制器
```

---

## 本版补齐的关键能力

|能力|是否补齐|
|---|---|
|Candidate Master Record|已补齐|
|Source Event|已补齐|
|Identity Resolution|已补齐|
|Pool Identity|已补齐|
|Discovery Context|已补齐|
|Intake Time Context|已补齐|
|Dedup Resolution|已补齐|
|Source Quality|已补齐|
|Intake Quality|已补齐|
|Gap Policy|已补齐|
|Hard Negative Rules|已补齐|
|P02 Data Request|已补齐|
|Handoff Contract|已补齐|
|Test Matrix|已补齐|
|Report Model|已补齐|
|HER Execution Protocol|已补齐|

---

# 24. 仍然未解决的问题

|问题|当前状态|后续处理|
|---|---|---|
|candidate_id 生成器未代码化|已定义规则|Runner / Tool Binding 阶段实现|
|real GMGN 输入字段未完全对齐|P01 只定义需求|P02 / Tool Binding 真实对齐|
|legacy candidate mapping 未扫描|已定义接入位置|legacy mapping 工程任务|
|Telegram command 输入未绑定|已定义来源类型|Bot / Tool Binding 阶段|
|P01 acceptance validator 未实现|已定义标准|后续实现 validator|
|P01 → P02 handoff 未联调|需要 P02|下一阶段展开 P02|
|source quality 权重未回测|初始模型|Review / Upgrade 后校准|

---

# 本次认知升级点

1. **P01 的本质是候选主数据治理，不是候选发现。**
    
2. **P01 必须输出 P02 Data Request Packet。**  
    这是专业系统的关键：P01 发现缺什么，P02 才知道要补什么。
    
3. **候选来源必须事件化。**  
    一个 token 可以多次被发现，每次发现都要成为 source event，而不是覆盖主记录。
    
4. **candidate master record 是 P01 的核心资产。**
    
5. **去重不是简单查重，而是 identity resolution + dedup resolution + rediscovery merge。**
    
6. **发现时上下文必须保留。**  
    discovery market cap、liquidity、token age 缺失不能假装有，必须交给 P02 补。
    
7. **P01 的 READY_WITH_GAPS 是正常专业状态。**  
    它不阻断进入 P02，但必须带 gap 和 limitation。
    
8. **P01 只能交接给 P02。**  
    任何跳到证据、场景、策略、paper runtime 的路径都必须阻断。