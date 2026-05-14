# P01 数据事实层认知升级版

## 从“数据采集层”升级为“数据源情报控制层”

---

# 0. 核心结论

你判断得对。

如果 P02 都要升级成：

```text
图模型 + 概率推断 + 多角色审计 + 时序诊断 + replay 校准
```

那么 P01 不能再只是：

```text
GMGN / OKX 接口采集
raw 落盘
normalized 标准化
quality gate
handoff packet
```

这只是 **工程化数据采集层**，还不是专业化数据事实层。

真正专业的 P01 应该升级成：

```text
P01_data_source_intelligence_controller
=
数据源注册
+ 连接健康检测
+ 采集调度
+ 原始快照保存
+ schema 漂移检测
+ 字段血缘图
+ 数据新鲜度模型
+ 数据完整度概率模型
+ 跨源一致性校验
+ 数据源可靠性评分
+ 缺口根因诊断
+ 回补 / replay / 降级策略
+ 下游权限裁决
```

也就是说：

> **P01 不只是“拿到数据”，而是判断数据是否足以成为系统事实。**

---

# 1. P01 新定位

## 旧定位

```text
P01 = 数据采集 + 标准化 + handoff
```

这只能解决：

```text
系统有没有数据
```

---

## 新定位

```text
P01 = 数据源情报控制层
```

它要解决：

```text
数据从哪里来？
数据是否真实？
数据是否完整？
数据是否新鲜？
数据源是否稳定？
字段是否发生变化？
多个来源是否冲突？
缺失数据的原因是什么？
哪些判断可以继续？
哪些判断必须暂停？
哪些数据需要回补？
哪些输出只能 replay？
```

---

# 2. P01 专业化目标

P01 的专业标准不应该是：

```text
能拉到 GMGN / OKX 数据
```

而应该是：

```text
每个字段都有来源
每个字段都有时间戳
每个字段都有置信度
每个字段都有缺失原因
每个字段都能追踪到 raw 证据
每个数据源都有健康状态
每个 token 都有数据完整度诊断
每个下游阶段都有读取权限裁决
每次失败都能定位根因
每次运行都能 replay
```

---

# 3. P01 应升级为 12 个专业子系统

```text
P01 数据源情报控制层
├── P01-00 阶段身份与运行边界
├── P01-01 数据源注册与能力矩阵
├── P01-02 数据源健康与 SLA 模型
├── P01-03 采集调度与优先级模型
├── P01-04 原始快照与事件溯源
├── P01-05 Schema 漂移与字段合约检测
├── P01-06 字段血缘图与来源可信度
├── P01-07 时间新鲜度与多快照版本管理
├── P01-08 跨源一致性与冲突仲裁
├── P01-09 数据完整度 / 置信度概率模型
├── P01-10 缺口根因诊断与回补计划
├── P01-11 下游权限裁决与 handoff packet
└── P01-12 Replay / 校准 / 数据质量复盘
```

这才是 P01 的专业化结构。

---

# 4. P01 的“专业计算大脑”模型群

P01 也需要模型大脑，不只是 if/else 检查。

建议命名：

```text
P01_data_source_intelligence_brain
```

中文：

```text
P01 数据源情报计算大脑
```

---

## 4.1 Source Reliability Model｜数据源可靠性模型

回答：

```text
GMGN 当前可靠吗？
OKX 当前可靠吗？
这个数据源过去是否经常失败？
是否存在延迟、限流、空返回、字段变化？
```

### 计算维度

|指标|含义|
|---|---|
|`availability_score`|可用率|
|`latency_score`|响应速度|
|`success_rate_score`|成功率|
|`schema_stability_score`|字段稳定度|
|`freshness_score`|数据新鲜度|
|`historical_failure_score`|历史失败率|
|`source_consistency_score`|与其他源一致性|

### 输出

```json
{
  "source_id": "gmgn",
  "source_reliability_score": 0.86,
  "availability_score": 0.91,
  "latency_score": 0.78,
  "schema_stability_score": 0.92,
  "freshness_score": 0.88,
  "current_status": "SOURCE_RELIABLE",
  "failure_risk": "LOW"
}
```

---

## 4.2 Schema Drift Detection｜字段漂移检测模型

回答：

```text
GMGN / OKX 返回字段有没有变？
字段类型有没有变？
字段路径有没有变？
字段语义有没有可能变？
```

### 检测内容

```text
字段新增
字段缺失
字段类型变化
字段路径变化
字段值域异常
字段单位变化
字段含义疑似变化
```

### 输出

```json
{
  "schema_status": "SCHEMA_STABLE",
  "detected_changes": [],
  "contract_impact": "NO_IMPACT",
  "downstream_risk": "LOW"
}
```

如果异常：

```json
{
  "schema_status": "SCHEMA_DRIFT_DETECTED",
  "detected_changes": [
    {
      "field": "market_cap_usd",
      "change_type": "TYPE_CHANGED",
      "expected_type": "number",
      "actual_type": "string",
      "impact": "MARKET_FACT_NORMALIZATION_BLOCKED"
    }
  ],
  "decision": "DATA_SCHEMA_REVIEW"
}
```

---

## 4.3 Data Freshness Model｜数据新鲜度模型

P01 必须区分不同字段的过期标准。

|数据类型|新鲜度要求|
|---|---|
|quote / price|秒级 / 分钟级|
|trade events|分钟级|
|holder list|分钟到小时级|
|wallet profile|小时到天级|
|token profile|相对稳定|
|security scan|每轮执行前必须刷新|

### 输出

```json
{
  "token_address": "...",
  "freshness_status": "FRESH_ENOUGH",
  "fields": {
    "quote_price": {
      "age_sec": 12,
      "max_allowed_age_sec": 60,
      "status": "FRESH"
    },
    "holder_list": {
      "age_sec": 480,
      "max_allowed_age_sec": 900,
      "status": "FRESH"
    },
    "wallet_profile": {
      "age_sec": 7200,
      "max_allowed_age_sec": 86400,
      "status": "ACCEPTABLE"
    }
  }
}
```

---

## 4.4 Field Provenance Graph｜字段血缘图

P01 不应该只记录字段来源字符串，而要建立字段血缘图。

```text
raw payload
  ↓
field extraction
  ↓
normalization
  ↓
derived field
  ↓
handoff packet
  ↓
downstream consumer
```

### 输出

```json
{
  "field": "market_cap_change_from_discovery_pct",
  "lineage": [
    {
      "step": "raw",
      "source": "gmgn.token_profile_raw.market_cap_usd"
    },
    {
      "step": "system_snapshot",
      "source": "candidate_first_seen.market_cap_usd"
    },
    {
      "step": "derived",
      "formula": "(current_market_cap - discovery_market_cap) / discovery_market_cap"
    },
    {
      "step": "normalized",
      "target": "normalized_market_fact.market_cap_change_from_discovery_pct"
    }
  ],
  "confidence": 0.82
}
```

专业价值：

```text
后续任何判断都能追溯到原始字段。
```

---

## 4.5 Cross-source Reconciliation｜跨源一致性仲裁模型

GMGN 和 OKX 的价格、市值、流动性可能不一致。

P01 要判断：

```text
哪个源优先？
偏差是否正常？
是否需要暂停？
是否需要降级？
```

### 输出

```json
{
  "price_reconciliation": {
    "gmgn_price_usd": 0.00125,
    "okx_price_usd": 0.00131,
    "deviation_pct": 4.8,
    "status": "ACCEPTABLE_DEVIATION",
    "selected_primary_source": "okx",
    "fallback_source": "gmgn"
  },
  "decision": "PRICE_FACT_USABLE"
}
```

如果偏差过大：

```json
{
  "deviation_pct": 28.4,
  "status": "HIGH_SOURCE_CONFLICT",
  "decision": "MARKET_FACT_PAUSE",
  "downstream_permission": {
    "paper_trading": false,
    "market_structure_analysis": "LIMITED"
  }
}
```

---

## 4.6 Data Completeness Probability Model｜数据完整度概率模型

不是简单说字段有 / 没有，而是判断：

```text
这个 token 当前数据足不足以支持 P02 / P03 / P06？
```

### 输出

```json
{
  "token_address": "...",
  "completeness_probability": {
    "for_p02_wallet_structure": 0.81,
    "for_p03_market_structure": 0.76,
    "for_p06_paper_trading": 0.63
  },
  "missing_critical_fields": [
    "funding_relation_edges"
  ],
  "decision": {
    "P02": "ALLOW_WITH_LIMITATIONS",
    "P03": "ALLOW",
    "P06": "PAUSE"
  }
}
```

---

## 4.7 Missing Data Root Cause Model｜缺失数据根因模型

P01 不能只说：

```text
字段缺失
```

要说清楚缺失原因：

|根因|含义|
|---|---|
|`SOURCE_NOT_AVAILABLE`|数据源不可用|
|`SOURCE_DOES_NOT_SUPPORT_FIELD`|数据源本身不支持|
|`SCHEMA_CHANGED`|字段结构变化|
|`TOKEN_TOO_NEW`|token 太新，数据尚未生成|
|`LOW_LIQUIDITY_NO_ROUTE`|流动性不足，无报价|
|`FETCH_TIMEOUT`|获取超时|
|`RATE_LIMITED`|限流|
|`NORMALIZATION_FAILED`|标准化失败|
|`FIELD_CONFLICT`|多源冲突|
|`CACHE_STALE`|缓存过期|

### 输出

```json
{
  "missing_field": "funding_relation_edges",
  "root_cause": "SOURCE_DOES_NOT_SUPPORT_FIELD",
  "impact": "P02 same-source confidence capped at MEDIUM",
  "resolution_plan": "Use behavior similarity model until funding source data available",
  "priority": "HIGH"
}
```

---

## 4.8 Acquisition Priority Model｜采集优先级模型

不是所有 token 都同等采集。

P01 要根据候选状态决定优先级。

|优先级|条件|
|---|---|
|`P0_URGENT`|即将进入 P05 / P06 的 token|
|`P1_HIGH`|P02/P03 已支持但缺 quote|
|`P2_NORMAL`|普通候选|
|`P3_BACKGROUND`|观察池|
|`P4_REPLAY_ONLY`|仅回放样本|

### 输出

```json
{
  "token_address": "...",
  "acquisition_priority": "P1_HIGH",
  "reason": "P02 wallet structure support exists but quote freshness expired",
  "required_fetches": [
    "okx.quote",
    "okx.liquidity",
    "gmgn.trade_events"
  ]
}
```

---

## 4.9 Data Quality Decision Brain｜数据质量裁决大脑

最终 P01 不应只用一个 `coverage_score`，而要综合：

```text
数据源可靠性
字段完整度
字段新鲜度
字段血缘
schema 稳定度
跨源一致性
缺失根因
下游需求
```

输出：

```json
{
  "data_fact_status": "DATA_READY_WITH_LIMITATIONS",
  "decision_reason": "Core token, market and wallet facts available; funding relation missing limits same-source confirmation.",
  "downstream_permissions": {
    "P02_wallet_chip_structure_controller": "ALLOW_LIMITED",
    "P03_market_structure_controller": "ALLOW",
    "P04_scenario_recognition_controller": "ALLOW",
    "P05_strategy_gate_controller": "PAUSE",
    "P06_paper_trading_controller": "PAUSE",
    "P07_real_execution_controller": false
  }
}
```

---

# 5. P01 专业阶段时间设计

这里分成两类：

1. **系统建设阶段时间**
2. **单次运行时间轴**

---

# 5.1 系统建设阶段时间

## Phase P01-T0：阶段身份与边界建立

目标：

```text
让 HER 先知道 P01 是数据源情报控制层，不是普通采集脚本。
```

输出：

```text
phase_01_data_source_intelligence_controller.yaml
phase_01_data_source_intelligence_controller.md
```

必须定义：

```text
阶段职责
非职责
数据源
下游消费者
状态码
失败策略
权限边界
real_execution=false
```

---

## Phase P01-T1：Source Registry 与能力矩阵

目标：

```text
把 GMGN / OKX / manual / cache / replay 的能力边界一次性定义清楚。
```

输出：

```text
source_registry/
  gmgn_source_profile.yaml
  okx_source_profile.yaml
  manual_input_source_profile.yaml
  local_cache_source_profile.yaml
  replay_fixture_source_profile.yaml
  source_capability_matrix.json
```

---

## Phase P01-T2：Source Health 与 SLA 模型

目标：

```text
建立数据源可靠性评分，而不是只判断连不连得上。
```

输出：

```text
source_health/
  gmgn_source_health_report.json
  okx_source_health_report.json
  source_reliability_scorecard.json
  source_sla_report.json
```

状态：

```text
SOURCE_RELIABLE
SOURCE_DEGRADED
SOURCE_UNSTABLE
SOURCE_BLOCKED
SOURCE_SCHEMA_REVIEW
```

---

## Phase P01-T3：采集调度与优先级系统

目标：

```text
决定先采集哪些 token、哪些字段、哪些源。
```

输出：

```text
acquisition_planner/
  acquisition_priority_queue.json
  token_fetch_plan.json
  source_fetch_schedule.json
  fetch_dependency_graph.json
```

关键能力：

```text
优先采集临近下游判断的 token
对过期字段重新采集
对失败字段安排重试
对低价值候选降低频率
```

---

## Phase P01-T4：Raw Snapshot 与事件溯源

目标：

```text
所有外部返回先保存 raw，形成不可篡改证据层。
```

输出：

```text
raw/
  gmgn/<token>/
  okx/<token>/
raw_snapshot_manifest.json
raw_event_log.jsonl
```

每次采集必须记录：

```text
source_id
endpoint_or_skill
request_params
request_hash
fetched_at
response_status
record_count
payload_hash
error_type
```

---

## Phase P01-T5：Schema Drift 与合约检测

目标：

```text
防止 GMGN / OKX 字段变化后污染系统。
```

输出：

```text
schema_monitor/
  schema_diff_report.json
  schema_validation_report.json
  schema_drift_events.jsonl
  contract_impact_report.json
```

---

## Phase P01-T6：Normalization 与字段血缘图

目标：

```text
把 raw 转为 normalized，并记录每个字段血缘。
```

输出：

```text
normalized/<token>/
  normalized_token_fact.json
  normalized_market_fact.json
  normalized_wallet_fact.json
  normalized_quote_fact.json
  normalized_fact_manifest.json

lineage/<token>/
  field_lineage_graph.json
  field_provenance_report.json
```

---

## Phase P01-T7：Freshness 与多快照版本管理

目标：

```text
判断每个字段是否过期，并保存多轮快照用于变化判断。
```

输出：

```text
temporal/
  snapshot_index.json
  field_freshness_report.json
  multi_snapshot_delta_report.json
  stale_field_events.jsonl
```

核心能力：

```text
当前值
上一快照
发现时值
最高值
最低值
变化速度
字段年龄
是否过期
```

---

## Phase P01-T8：Cross-source Reconciliation

目标：

```text
处理 GMGN / OKX 之间的数据冲突。
```

输出：

```text
reconciliation/<token>/
  price_reconciliation_report.json
  liquidity_reconciliation_report.json
  security_reconciliation_report.json
  source_conflict_events.jsonl
```

---

## Phase P01-T9：Data Quality Brain

目标：

```text
输出真正的数据质量裁决，而不是简单 completeness。
```

输出：

```text
quality/<token>/
  data_completeness_probability_report.json
  data_confidence_report.json
  data_quality_decision.json
  missing_data_root_cause_report.json
```

---

## Phase P01-T10：Handoff Packet 与下游权限

目标：

```text
把 P01 裁决转成下游可读取的正式交接包。
```

输出：

```text
handoff/<token>/
  data_fact_handoff_packet.json
  downstream_permission_matrix.json
  downstream_readiness_report.md
```

---

## Phase P01-T11：Replay Fixture 与回补机制

目标：

```text
上游失败时，系统还能离线验证。
```

输出：

```text
replay_fixture/
  fixture_manifest.json
  fixture_tokens/
  replay_validation_report.json

backfill/
  backfill_plan.json
  backfill_status_report.json
```

---

## Phase P01-T12：P01 日报 / 审计 / 校准

目标：

```text
让 P01 自己能复盘数据质量。
```

输出：

```text
audit/
  p01_runtime_log.jsonl
  p01_error_events.jsonl
  p01_data_quality_events.jsonl
  p01_daily_report.md
  p01_gap_audit_report.md
  p01_completion_report.md
```

---

# 5.2 单次运行时间轴

每一次系统运行，P01 应按这个顺序执行。

```text
T00 加载阶段身份
T01 加载 source registry
T02 检查 GMGN / OKX source health
T03 读取候选 token universe
T04 计算采集优先级
T05 生成 token_fetch_plan
T06 执行 GMGN raw fetch
T07 执行 OKX raw fetch
T08 写入 raw snapshot manifest
T09 执行 schema validation
T10 执行 normalization
T11 构建 field lineage graph
T12 执行 freshness check
T13 执行 cross-source reconciliation
T14 执行 data completeness probability model
T15 执行 missing data root cause diagnosis
T16 输出 data_quality_decision
T17 输出 data_fact_handoff_packet
T18 更新 replay fixture / backfill plan
T19 输出 runtime audit report
T20 通知下游 P02/P03/P06 可读权限
```

---

# 6. P01 输出目录升级版

```text
p01_data_fact/
├── phase_identity/
│   ├── phase_01_data_source_intelligence_controller.yaml
│   └── phase_01_data_source_intelligence_controller.md
│
├── source_registry/
│   ├── gmgn_source_profile.yaml
│   ├── okx_source_profile.yaml
│   ├── source_capability_matrix.json
│   └── source_dependency_graph.json
│
├── source_health/
│   ├── gmgn_source_health_report.json
│   ├── okx_source_health_report.json
│   ├── source_reliability_scorecard.json
│   └── source_sla_report.json
│
├── acquisition_planner/
│   ├── acquisition_priority_queue.json
│   ├── token_fetch_plan.json
│   ├── source_fetch_schedule.json
│   └── fetch_dependency_graph.json
│
├── raw/
│   ├── gmgn/<token_address>/
│   ├── okx/<token_address>/
│   ├── raw_snapshot_manifest.json
│   └── raw_event_log.jsonl
│
├── schema_monitor/
│   ├── schema_diff_report.json
│   ├── schema_validation_report.json
│   ├── schema_drift_events.jsonl
│   └── contract_impact_report.json
│
├── normalized/
│   └── <token_address>/
│       ├── normalized_token_fact.json
│       ├── normalized_market_fact.json
│       ├── normalized_wallet_fact.json
│       ├── normalized_quote_fact.json
│       └── normalized_fact_manifest.json
│
├── lineage/
│   └── <token_address>/
│       ├── field_lineage_graph.json
│       ├── field_provenance_report.json
│       └── derived_field_formula_manifest.json
│
├── temporal/
│   └── <token_address>/
│       ├── snapshot_index.json
│       ├── field_freshness_report.json
│       ├── multi_snapshot_delta_report.json
│       └── stale_field_events.jsonl
│
├── reconciliation/
│   └── <token_address>/
│       ├── price_reconciliation_report.json
│       ├── liquidity_reconciliation_report.json
│       ├── security_reconciliation_report.json
│       └── source_conflict_events.jsonl
│
├── quality/
│   └── <token_address>/
│       ├── data_completeness_probability_report.json
│       ├── data_confidence_report.json
│       ├── data_quality_decision.json
│       ├── missing_data_root_cause_report.json
│       └── p01_data_quality_brain_trace.json
│
├── handoff/
│   └── <token_address>/
│       ├── data_fact_handoff_packet.json
│       ├── downstream_permission_matrix.json
│       └── downstream_readiness_report.md
│
├── replay_fixture/
│   ├── fixture_manifest.json
│   ├── fixture_tokens/
│   └── replay_validation_report.json
│
├── backfill/
│   ├── backfill_plan.json
│   ├── backfill_status_report.json
│   └── unresolved_data_gap_queue.json
│
└── audit/
    ├── p01_runtime_log.jsonl
    ├── p01_error_events.jsonl
    ├── p01_data_quality_events.jsonl
    ├── p01_daily_report.md
    ├── p01_gap_audit_report.md
    └── p01_completion_report.md
```

---

# 7. P01 专业状态码升级

## 数据源状态

```text
SOURCE_RELIABLE
SOURCE_DEGRADED
SOURCE_UNSTABLE
SOURCE_BLOCKED
SOURCE_SCHEMA_REVIEW
SOURCE_RATE_LIMITED
SOURCE_REPLAY_ONLY
```

## 字段状态

```text
FIELD_PRESENT
FIELD_MISSING_REQUIRED
FIELD_MISSING_OPTIONAL
FIELD_STALE
FIELD_CONFLICTED
FIELD_SCHEMA_CHANGED
FIELD_SOURCE_LIMITED
FIELD_DERIVED
FIELD_LOW_CONFIDENCE
```

## Token 数据状态

```text
DATA_READY
DATA_READY_WITH_LIMITATIONS
DATA_PARTIAL_READY
DATA_PAUSE
DATA_BLOCK
DATA_SCHEMA_REVIEW
DATA_REPLAY_ONLY
DATA_BACKFILL_REQUIRED
```

## 下游权限状态

```text
ALLOW
ALLOW_LIMITED
PAUSE
BLOCK
REPLAY_ONLY
SCHEMA_REVIEW_REQUIRED
```

---

# 8. P01 下游权限裁决矩阵

|P01 状态|P02 钱包结构|P03 市场结构|P05 策略门禁|P06 纸面交易|
|---|---|---|---|---|
|`DATA_READY`|允许|允许|可继续|可继续|
|`DATA_READY_WITH_LIMITATIONS`|限制允许|允许|暂停或限制|暂停|
|`DATA_PARTIAL_READY`|限制允许|限制允许|暂停|暂停|
|`DATA_PAUSE`|暂停|暂停|阻断|阻断|
|`DATA_BLOCK`|阻断|阻断|阻断|阻断|
|`DATA_SCHEMA_REVIEW`|阻断|阻断|阻断|阻断|
|`DATA_REPLAY_ONLY`|replay|replay|禁止|禁止|
|`DATA_BACKFILL_REQUIRED`|等待补数据|视情况|暂停|暂停|

---

# 9. P01 关键输出：升级版 `data_fact_handoff_packet.json`

新版 handoff 不应该只是路径列表，而是完整数据事实裁决包。

```json
{
  "schema_version": "P01_DATA_SOURCE_INTELLIGENCE_V2",
  "phase_id": "P01",
  "run_id": "20260513_100000",
  "token_address": "...",
  "chain": "solana",

  "data_fact_status": "DATA_READY_WITH_LIMITATIONS",

  "source_health": {
    "gmgn": {
      "status": "SOURCE_RELIABLE",
      "reliability_score": 0.86,
      "latency_ms": 820,
      "schema_status": "SCHEMA_STABLE",
      "last_success_at": "..."
    },
    "okx": {
      "status": "SOURCE_DEGRADED",
      "reliability_score": 0.71,
      "latency_ms": 1100,
      "schema_status": "SCHEMA_STABLE",
      "last_success_at": "..."
    }
  },

  "normalized_files": {
    "token_fact": "p01_data_fact/normalized/<token>/normalized_token_fact.json",
    "market_fact": "p01_data_fact/normalized/<token>/normalized_market_fact.json",
    "wallet_fact": "p01_data_fact/normalized/<token>/normalized_wallet_fact.json",
    "quote_fact": "p01_data_fact/normalized/<token>/normalized_quote_fact.json"
  },

  "lineage_files": {
    "field_lineage_graph": "p01_data_fact/lineage/<token>/field_lineage_graph.json",
    "field_provenance_report": "p01_data_fact/lineage/<token>/field_provenance_report.json"
  },

  "temporal_files": {
    "field_freshness_report": "p01_data_fact/temporal/<token>/field_freshness_report.json",
    "multi_snapshot_delta_report": "p01_data_fact/temporal/<token>/multi_snapshot_delta_report.json"
  },

  "quality_brain": {
    "completeness_probability": {
      "for_p02_wallet_structure": 0.81,
      "for_p03_market_structure": 0.76,
      "for_p06_paper_trading": 0.63
    },
    "confidence_score": 0.78,
    "source_conflict_level": "LOW",
    "missing_critical_fields": [],
    "missing_limited_fields": [
      "funding_relation_edges"
    ],
    "decision_reason": "Core token, wallet and market facts are usable; funding relation data missing limits same-source confidence."
  },

  "downstream_permissions": {
    "P02_wallet_chip_structure_controller": "ALLOW_LIMITED",
    "P03_market_structure_controller": "ALLOW",
    "P04_scenario_recognition_controller": "ALLOW",
    "P05_strategy_gate_controller": "PAUSE",
    "P06_paper_trading_controller": "PAUSE",
    "P07_real_execution_controller": false
  },

  "handoff_constraints": {
    "raw_direct_access_allowed": false,
    "real_execution_allowed": false,
    "replay_only": false,
    "requires_backfill": true,
    "requires_human_review": false
  },

  "backfill_plan": {
    "required": true,
    "missing_fields": [
      "funding_relation_edges"
    ],
    "priority": "HIGH",
    "impact": "same-source confirmation confidence capped"
  }
}
```

---

# 10. P01 多角色审计设计

P01 也需要角色系统，不只是 P02。

## 10.1 数据源工程师

负责：

```text
GMGN / OKX 是否可连接？
是否限流？
是否超时？
是否字段变化？
```

输出：

```text
source_engineer_report.json
```

---

## 10.2 数据质量官

负责：

```text
数据是否完整？
是否新鲜？
是否可交付下游？
```

输出：

```text
data_quality_officer_report.json
```

---

## 10.3 Schema 合约审计官

负责：

```text
字段结构是否符合 contract？
是否发生 schema drift？
是否会影响下游？
```

输出：

```text
schema_contract_auditor_report.json
```

---

## 10.4 字段血缘官

负责：

```text
每个字段是否能追踪 raw 来源？
派生字段公式是否明确？
字段置信度是否合理？
```

输出：

```text
field_lineage_officer_report.json
```

---

## 10.5 时间一致性官

负责：

```text
字段是否过期？
不同字段时间是否错位？
是否用旧 holder 搭配新 quote？
```

输出：

```text
temporal_consistency_officer_report.json
```

---

## 10.6 跨源仲裁官

负责：

```text
GMGN / OKX 冲突时用谁？
价格偏差是否可接受？
流动性冲突是否阻断 paper？
```

输出：

```text
source_reconciliation_officer_report.json
```

---

## 10.7 下游权限官

负责：

```text
P02 / P03 / P05 / P06 是否可以读取？
是 full、limited、pause 还是 block？
```

输出：

```text
downstream_permission_officer_report.json
```

---

# 11. P01 专业验收标准

## 11.1 不再接受的低标准

```text
能跑脚本
能生成 raw
能生成 normalized
能生成 handoff
```

这只是基础。

---

## 11.2 专业验收标准

必须达到：

```text
1. 每个数据源有可靠性评分
2. 每个字段有来源血缘
3. 每个字段有 freshness 状态
4. 每个字段缺失有 root cause
5. 每个 token 有 completeness probability
6. 每个 token 有 cross-source reconciliation
7. 每次 schema 变化能被检测
8. 每个下游阶段有权限裁决
9. 每次失败能进入 backfill 或 replay
10. 每日输出 P01 数据质量日报
```

---

# 12. HER 可复制执行任务书

```text
任务名称：
P01_data_source_intelligence_controller 专业数据源情报控制层升级任务

任务目标：
将 P01 从普通 GMGN / OKX 数据采集层升级为专业数据源情报控制层。P01 不仅要采集数据，还要判断数据源可靠性、字段血缘、schema 稳定性、数据新鲜度、跨源一致性、字段完整度概率、缺失根因、回补计划、replay 能力和下游读取权限。P01 的最终目标不是“拿到数据”，而是生成可被 P02/P03/P04/P05/P06 信任的数据事实裁决包。

核心原则：
1. P01 不是接口脚本集合，而是数据源情报控制器。
2. 所有 GMGN / OKX 返回必须先进入 raw snapshot。
3. 所有 normalized 字段必须有 field lineage。
4. 所有字段必须有 source、fetched_at、confidence、freshness_status、missing_reason。
5. 数据源必须有 reliability score。
6. schema 变化必须被检测并阻断下游。
7. GMGN / OKX 冲突必须进入 reconciliation。
8. 缺失字段必须进入 missing root cause，不允许静默忽略。
9. 下游权限必须由 P01 裁决，不允许下游自行判断可用性。
10. real_execution 必须固定 false。

新增目录：
/root/sikk-gmgn/data/gmgn_candidates_live_run/p01_data_fact/

需要包含：
phase_identity/
source_registry/
source_health/
acquisition_planner/
raw/
schema_monitor/
normalized/
lineage/
temporal/
reconciliation/
quality/
handoff/
replay_fixture/
backfill/
audit/

新增代码目录：
/root/sikk-gmgn/controllers/
/root/sikk-gmgn/models/p01_source_intelligence/
/root/sikk-gmgn/diagnostics/p01/
/root/sikk-gmgn/auditors/p01/

新增核心代码文件：
/root/sikk-gmgn/controllers/p01_data_source_intelligence_controller.py
/root/sikk-gmgn/models/p01_source_intelligence/source_reliability_model.py
/root/sikk-gmgn/models/p01_source_intelligence/schema_drift_detector.py
/root/sikk-gmgn/models/p01_source_intelligence/data_freshness_model.py
/root/sikk-gmgn/models/p01_source_intelligence/field_lineage_graph_builder.py
/root/sikk-gmgn/models/p01_source_intelligence/cross_source_reconciliation_model.py
/root/sikk-gmgn/models/p01_source_intelligence/data_completeness_probability_model.py
/root/sikk-gmgn/models/p01_source_intelligence/missing_data_root_cause_model.py
/root/sikk-gmgn/models/p01_source_intelligence/acquisition_priority_model.py
/root/sikk-gmgn/models/p01_source_intelligence/data_quality_decision_brain.py

第一阶段：P01-T0 阶段身份
创建：
- phase_01_data_source_intelligence_controller.yaml
- phase_01_data_source_intelligence_controller.md

必须写明：
- P01 是数据源情报控制层
- P01 不负责策略判断
- P01 不负责钱包结构判断
- P01 不负责 paper entry
- P01 负责数据源、字段、时间、血缘、质量、权限

第二阶段：P01-T1 Source Registry
创建：
- gmgn_source_profile.yaml
- okx_source_profile.yaml
- source_capability_matrix.json
- source_dependency_graph.json

第三阶段：P01-T2 Source Health
实现 source_reliability_model。
输出：
- gmgn_source_health_report.json
- okx_source_health_report.json
- source_reliability_scorecard.json
- source_sla_report.json

状态包括：
- SOURCE_RELIABLE
- SOURCE_DEGRADED
- SOURCE_UNSTABLE
- SOURCE_BLOCKED
- SOURCE_SCHEMA_REVIEW

第四阶段：P01-T3 Acquisition Planner
实现 acquisition_priority_model。
输出：
- acquisition_priority_queue.json
- token_fetch_plan.json
- source_fetch_schedule.json
- fetch_dependency_graph.json

第五阶段：P01-T4 Raw Snapshot
所有外部数据必须先保存 raw。
输出：
- gmgn raw
- okx raw
- raw_snapshot_manifest.json
- raw_event_log.jsonl

第六阶段：P01-T5 Schema Drift
实现 schema_drift_detector。
输出：
- schema_diff_report.json
- schema_validation_report.json
- schema_drift_events.jsonl
- contract_impact_report.json

第七阶段：P01-T6 Normalization + Lineage
实现 field_lineage_graph_builder。
输出：
- normalized_token_fact.json
- normalized_market_fact.json
- normalized_wallet_fact.json
- normalized_quote_fact.json
- field_lineage_graph.json
- field_provenance_report.json
- derived_field_formula_manifest.json

第八阶段：P01-T7 Temporal Freshness
实现 data_freshness_model。
输出：
- snapshot_index.json
- field_freshness_report.json
- multi_snapshot_delta_report.json
- stale_field_events.jsonl

第九阶段：P01-T8 Cross-source Reconciliation
实现 cross_source_reconciliation_model。
输出：
- price_reconciliation_report.json
- liquidity_reconciliation_report.json
- security_reconciliation_report.json
- source_conflict_events.jsonl

第十阶段：P01-T9 Data Quality Brain
实现：
- data_completeness_probability_model
- missing_data_root_cause_model
- data_quality_decision_brain

输出：
- data_completeness_probability_report.json
- data_confidence_report.json
- missing_data_root_cause_report.json
- p01_data_quality_brain_trace.json
- data_quality_decision.json

第十一阶段：P01-T10 Handoff Packet
升级 data_fact_handoff_packet.json。
必须包含：
- source_health
- normalized_files
- lineage_files
- temporal_files
- quality_brain
- downstream_permissions
- handoff_constraints
- backfill_plan

第十二阶段：P01-T11 Replay / Backfill
输出：
- fixture_manifest.json
- replay_validation_report.json
- backfill_plan.json
- backfill_status_report.json
- unresolved_data_gap_queue.json

第十三阶段：P01-T12 Audit
输出：
- p01_runtime_log.jsonl
- p01_error_events.jsonl
- p01_data_quality_events.jsonl
- p01_daily_report.md
- p01_gap_audit_report.md
- p01_completion_report.md

运行命令：
cd /root/sikk-gmgn

python3 controllers/p01_data_source_intelligence_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode init-phase

python3 controllers/p01_data_source_intelligence_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode source-health

python3 controllers/p01_data_source_intelligence_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode build-fetch-plan \
  --limit 50

python3 controllers/p01_data_source_intelligence_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode fetch-candidates \
  --limit 20

python3 controllers/p01_data_source_intelligence_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode normalize-and-lineage

python3 controllers/p01_data_source_intelligence_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode quality-brain

python3 controllers/p01_data_source_intelligence_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode build-handoff

python3 controllers/p01_data_source_intelligence_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode audit

pytest -q tests/p01/

验收标准：
1. GMGN / OKX 都有 source reliability score。
2. 每个 token 都有 raw snapshot。
3. 每个 normalized 字段都有 field lineage。
4. 每个字段都有 freshness 状态。
5. schema drift 能被检测。
6. GMGN / OKX 冲突能被 reconciliation。
7. 缺失字段有 root cause。
8. 每个 token 有 data completeness probability。
9. 每个 token 有 data_quality_decision。
10. 每个 token 有 data_fact_handoff_packet。
11. 下游权限由 P01 输出。
12. P02/P03/P06 不允许直接读 raw。
13. replay 和 backfill 机制存在。
14. 输出 p01_daily_report.md。
15. real_execution 必须 false。
```

---

# 13. 最终判断

按现在的认知标准，P01 应该从：

```text
数据采集层
```

升级为：

```text
数据源情报控制层
```

它的目标不是简单采集，而是：

```text
把外部不稳定数据源转化为系统内部可信事实
```

专业化 P01 必须具备：

```text
数据源可靠性判断
schema 漂移检测
字段血缘追踪
时间新鲜度管理
跨源冲突仲裁
完整度概率判断
缺失根因诊断
回补 / replay 策略
下游权限裁决
```

---

# 本次认知升级点

1. **P01 不是接口采集层，而是数据源情报控制层。**
2. **P01 的核心任务不是拿到数据，而是证明数据能不能成为事实。**
3. **P01 也需要计算大脑：source reliability、schema drift、freshness、lineage、reconciliation、completeness probability。**
4. **字段缺失要诊断根因，不只是记录 null。**
5. **多源冲突要仲裁，不是简单选一个来源。**
6. **每个字段都要有血缘图，后续 P02/P03/P06 才能审计。**
7. **P01 的 handoff packet 必须包含下游权限，而不是只包含文件路径。**
8. **P01 是后续所有专业判断的地基。P01 不专业，P02 再复杂也会被脏数据污染。**

# 尚未解决问题

1. GMGN 当前实际可用字段还需要由 HER 审计确认。
2. OKX 当前能否提供完整 quote / liquidity / route / security，需要实测。
3. `funding_relation_edges` 这类字段如果 P01 拿不到，P02 同源判断必须降级。
4. P01 的 source reliability 权重需要通过运行日志校准。
5. P01 的 replay fixture 至少需要 3-5 个真实 token 样本，否则专业模型无法稳定验证。