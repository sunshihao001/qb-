# P01 数据事实层专业版阶段包

## `P01_data_fact_controller`｜GMGN / OKX 数据源接入与事实层总控

---

# 0. 阶段总定位

## P01 的本质定义

```text
P01 数据事实层不是“数据说明文档”，也不是“接口脚本集合”。

P01 是系统事实入口控制器，负责把 GMGN、OKX、手动输入、历史缓存、replay 样本等上游来源，转化为可追溯、可审计、可质量判断、可交接给下游模块的标准事实数据包。
```

它负责回答：

```text
这个 token 的事实数据从哪里来？
什么时候获取？
是否完整？
是否新鲜？
是否可信？
是否存在字段缺失？
是否允许进入钱包结构分析？
是否允许进入行情结构分析？
是否允许进入 paper trading？
是否必须暂停、阻断或 replay？
```

---

# 1. P01 阶段核心结论

当前系统跑不起来 GMGN / OKX 代币数据，不能被理解为普通接口问题。它说明：

```text
P01 数据事实层尚未专业化成立。
```

正确处理方式不是继续补策略，而是先建立：

```text
P01_data_fact_controller
=
数据源登记
+ 数据源连接自检
+ 原始数据采集
+ 原始证据保存
+ 字段标准化
+ 数据质量门
+ 跨源一致性检查
+ 下游交接包
+ replay 样本
+ 运行审计
```

只有 P01 成立后，后续 P02 钱包结构、P03 市场结构、P04 场景识别、P05 策略门禁、P06 纸面交易才有真实输入。

---

# 2. P01 阶段身份文件

## 2.1 `phase_01_data_fact_controller.yaml`

这是阶段身份证，用于让 HER 明确这个阶段是谁、负责什么、权限边界是什么。

```yaml
phase_id: P01
phase_name: data_fact_controller
phase_cn_name: 数据事实层
phase_version: v2.0_professional
phase_type: schedulable_phase_controller

mission:
  primary_goal: >
    将 GMGN、OKX、手动输入、历史缓存、replay fixture 等上游数据源，
    转化为标准化、可追溯、可审计、可质量判断、可交接给下游的事实数据包。
  system_role: >
    作为 SIKK Stable Trader OS 的事实入口层，负责数据可信度、完整度、新鲜度、
    字段来源、失败状态、下游权限控制。

scope:
  responsible_for:
    - source_registry
    - source_connectivity_check
    - raw_data_ingestion
    - raw_snapshot_persistence
    - token_identity_normalization
    - market_fact_normalization
    - wallet_fact_normalization
    - quote_fact_normalization
    - source_provenance_tracking
    - data_freshness_check
    - data_coverage_check
    - cross_source_consistency_check
    - data_quality_gate
    - data_fact_handoff_packet
    - replay_fixture_generation
    - runtime_audit_report

  not_responsible_for:
    - wallet_role_final_classification
    - dominant_side_lifecycle_inference
    - market_pattern_final_decision
    - strategy_entry_signal_generation
    - paper_trade_decision
    - real_trade_execution
    - pnl_review
    - model_parameter_optimization

upstream_sources:
  gmgn:
    role: token_wallet_chip_behavior_fact_source
    permission: read_only
  okx:
    role: quote_liquidity_execution_feasibility_safety_source
    permission: read_only
  manual_input:
    role: human_supplied_candidate_source
    permission: read_only
  local_cache:
    role: historical_runtime_cache
    permission: read_only
  replay_fixture:
    role: offline_validation_sample
    permission: read_only

downstream_consumers:
  - P02_wallet_chip_structure_controller
  - P03_market_structure_controller
  - P04_scenario_recognition_controller
  - P05_strategy_gate_controller
  - P06_paper_trading_controller
  - P07_execution_risk_controller
  - P08_review_attribution_controller
  - dashboard_panel
  - explanation_module

core_outputs:
  - source_health_summary.json
  - candidate_token_universe.json
  - raw_snapshot_manifest.json
  - normalized_token_fact.json
  - normalized_market_fact.json
  - normalized_wallet_fact.json
  - normalized_quote_fact.json
  - data_coverage_report.json
  - freshness_report.json
  - field_provenance_report.json
  - cross_source_consistency_report.json
  - data_quality_decision.json
  - data_fact_handoff_packet.json
  - downstream_readiness_report.md
  - daily_data_source_report.md

hard_rules:
  - raw_data_must_be_persisted_before_normalization
  - downstream_modules_must_not_read_raw_external_payload_directly
  - missing_data_must_be_stateful_not_silent
  - stale_data_must_not_enter_trading_decision
  - schema_change_must_trigger_data_schema_review
  - real_execution_permission_must_be_false_in_P01
  - no_synthetic_data_allowed
  - fixture_data_must_be_marked_as_replay_only

phase_status_codes:
  - P01_NOT_STARTED
  - P01_SOURCE_REGISTRY_READY
  - P01_CONNECTIVITY_READY
  - P01_RAW_INGESTION_READY
  - P01_NORMALIZATION_READY
  - P01_QUALITY_GATE_READY
  - P01_HANDOFF_READY
  - P01_READY
  - P01_READY_WITH_WARNINGS
  - P01_BLOCKED
  - P01_SCHEMA_REVIEW_REQUIRED
  - P01_REPLAY_ONLY
```

---

## 2.2 `phase_01_data_fact_controller.md`

这是 HER 运行前必须读取的阶段上下文压缩包。

```markdown
# P01 数据事实层｜阶段上下文压缩包

P01 不是普通数据说明文档，而是 SIKK Stable Trader OS 的事实入口控制器。

当前阶段目标是把 GMGN / OKX / 手动输入 / 历史缓存 / replay fixture 转化为系统可用的标准事实包。

P01 的判断边界：

- P01 负责事实，不负责策略。
- P01 负责字段来源，不负责主观解释。
- P01 负责数据是否可用，不负责买卖判断。
- P01 负责下游权限，不负责执行交易。
- P01 负责失败状态，不允许静默忽略缺失字段。

GMGN 在 P01 中的定位：

GMGN 是 Token + Wallet + Chip + Behavior Fact Source，主要用于 token 基础信息、持有人、早期钱包、Top Holder、交易事件、智能资金、钱包行为、安全信息等事实输入。

OKX 在 P01 中的定位：

OKX 是 Quote + Liquidity + Execution Feasibility + Safety Cross-check Source，主要用于报价、流动性、路径可用性、执行可行性、安全扫描、价格交叉验证。

P01 的核心输出不是接口返回，而是 data_fact_handoff_packet.json。

所有下游阶段必须读取 handoff packet，而不是直接读取 GMGN / OKX raw。

如果数据缺失，P01 必须输出状态：

- DATA_READY
- DATA_PARTIAL_READY
- DATA_PAUSE
- DATA_BLOCK
- DATA_SCHEMA_REVIEW
- DATA_REPLAY_ONLY

禁止将缺失数据当成 0、false、空列表或默认安全。
```

---

# 3. P01 专业化设计原则

## 3.1 事实源优先原则

所有判断必须先回答：

```text
这个字段来自哪里？
```

不允许出现：

```text
字段存在，但不知道来源。
字段缺失，但系统继续判断。
字段过期，但系统继续使用。
字段来自 replay，但系统当实时数据使用。
```

---

## 3.2 Raw-first 原则

外部数据必须先进入 raw 层。

```text
GMGN / OKX 返回
  ↓
raw snapshot
  ↓
manifest
  ↓
normalization
  ↓
quality gate
  ↓
handoff packet
```

禁止：

```text
接口返回 → 策略判断
接口返回 → 钱包分类
接口返回 → paper runner
```

---

## 3.3 缺失状态化原则

数据缺失不是：

```text
0
false
null 后继续跑
空列表后继续判断
```

数据缺失必须成为系统状态：

```text
MISSING_REQUIRED_FIELD
SOURCE_UNAVAILABLE
FIELD_NOT_SUPPORTED_BY_SOURCE
SCHEMA_CHANGED
STALE_DATA
PARTIAL_DATA
```

---

## 3.4 Fail-closed 原则

如果关键事实缺失，系统默认阻断，而不是默认通过。

```text
无法确认安全 ≠ 安全
无法确认流动性 ≠ 可交易
无法确认钱包结构 ≠ 钱包结构正常
无法确认报价 ≠ 可以 paper entry
```

---

## 3.5 下游隔离原则

下游模块不关心 GMGN / OKX 怎么返回。

下游只关心：

```text
P01 是否允许我读取？
我应该读取哪个 normalized file？
这个 token 的数据状态是什么？
是否有阻断原因？
```

---

## 3.6 可复盘原则

每一次数据失败都必须可以回答：

```text
哪一个源失败？
什么时候失败？
什么参数失败？
失败类型是什么？
是否重试？
是否影响下游？
是否已经生成 replay fixture？
```

---

# 4. P01 总目录结构

建议统一放在：

```text
/root/sikk-gmgn/data/gmgn_candidates_live_run/p01_data_fact/
```

完整目录：

```text
p01_data_fact/
├── phase_identity/
│   ├── phase_01_data_fact_controller.yaml
│   └── phase_01_data_fact_controller.md
│
├── source_registry/
│   ├── gmgn_source_profile.yaml
│   ├── okx_source_profile.yaml
│   ├── manual_input_source_profile.yaml
│   ├── local_cache_source_profile.yaml
│   └── source_capability_matrix.json
│
├── connectivity/
│   ├── gmgn_connectivity_report.json
│   ├── okx_connectivity_report.json
│   ├── source_health_summary.json
│   └── source_connectivity_runtime_log.jsonl
│
├── candidate_universe/
│   ├── candidate_token_universe.json
│   ├── candidate_token_universe.csv
│   ├── candidate_token_universe.md
│   └── candidate_source_trace.jsonl
│
├── raw/
│   ├── gmgn/
│   │   └── <token_address>/
│   │       ├── token_profile_raw.json
│   │       ├── holder_list_raw.json
│   │       ├── top_holders_raw.json
│   │       ├── trade_events_raw.json
│   │       ├── wallet_profile_raw.json
│   │       ├── smart_money_raw.json
│   │       ├── security_raw.json
│   │       └── gmgn_fetch_manifest.json
│   │
│   ├── okx/
│   │   └── <token_address>/
│   │       ├── quote_raw.json
│   │       ├── liquidity_raw.json
│   │       ├── route_raw.json
│   │       ├── security_scan_raw.json
│   │       └── okx_fetch_manifest.json
│   │
│   └── raw_snapshot_manifest.json
│
├── normalized/
│   └── <token_address>/
│       ├── normalized_token_fact.json
│       ├── normalized_market_fact.json
│       ├── normalized_wallet_fact.json
│       ├── normalized_quote_fact.json
│       └── normalized_fact_manifest.json
│
├── quality/
│   └── <token_address>/
│       ├── data_coverage_report.json
│       ├── freshness_report.json
│       ├── field_provenance_report.json
│       ├── schema_validation_report.json
│       ├── cross_source_consistency_report.json
│       └── data_quality_decision.json
│
├── handoff/
│   └── <token_address>/
│       ├── data_fact_handoff_packet.json
│       ├── downstream_readiness_report.md
│       └── downstream_permission_matrix.json
│
├── replay_fixture/
│   ├── fixture_manifest.json
│   ├── fixture_tokens/
│   └── replay_validation_report.json
│
├── audit/
│   ├── data_source_runtime_log.jsonl
│   ├── source_error_events.jsonl
│   ├── data_quality_events.jsonl
│   ├── p01_phase_status.json
│   └── daily_data_source_report.md
│
└── reports/
    ├── p01_completion_report.md
    ├── p01_gap_audit_report.md
    └── p01_downstream_handoff_report.md
```

---

# 5. P01 子阶段总表

|子阶段|名称|核心任务|必须输出|
|---|---|---|---|
|P01-A|阶段身份层|定义阶段职责、边界、权限|`phase_01_data_fact_controller.yaml/md`|
|P01-B|数据源登记层|定义 GMGN/OKX 能力和字段边界|`source_capability_matrix.json`|
|P01-C|连接自检层|判断数据源是否可用|`source_health_summary.json`|
|P01-D|候选全集层|统一 token 候选来源|`candidate_token_universe.json`|
|P01-E|Raw 采集层|保存 GMGN/OKX 原始返回|`raw_snapshot_manifest.json`|
|P01-F|标准化层|统一字段结构|`normalized_*_fact.json`|
|P01-G|字段血缘层|记录字段来源、时间、置信度|`field_provenance_report.json`|
|P01-H|新鲜度层|判断数据是否过期|`freshness_report.json`|
|P01-I|覆盖率层|判断字段完整度|`data_coverage_report.json`|
|P01-J|跨源一致性层|判断 GMGN/OKX 是否冲突|`cross_source_consistency_report.json`|
|P01-K|数据质量门|决定是否允许下游读取|`data_quality_decision.json`|
|P01-L|下游交接层|输出统一 handoff packet|`data_fact_handoff_packet.json`|
|P01-M|Replay 层|保证离线可测试|`fixture_manifest.json`|
|P01-N|审计报告层|输出日报和失败归因|`daily_data_source_report.md`|

---

# 6. 数据源职责定义

## 6.1 GMGN 职责

GMGN 是结构事实源。

|数据类别|用途|下游|
|---|---|---|
|Token Profile|token 身份、创建时间、市值|P03 / P04|
|Holder List|持有人结构、集中度|P02|
|Top Holders|大户集中、Top Holder 风险|P02|
|Trade Events|早期钱包、买卖节奏、筹码迁移|P02 / P04|
|Wallet Profile|地址画像、历史行为|P02|
|Smart Money|智能资金参与|P02 / P04|
|Security|基础安全过滤|P05 / P07|
|Social / KOL|可选辅助信号|P04|

---

## 6.2 OKX 职责

OKX 是报价、流动性、执行可行性和安全校验源。

|数据类别|用途|下游|
|---|---|---|
|Quote|当前价格、paper entry price|P06|
|Liquidity|是否可成交、滑点估算|P05 / P06 / P07|
|Route|是否存在交易路径|P07|
|Security Scan|执行前风险检查|P05 / P07|
|Quote Timestamp|判断报价是否过期|P01 / P06|
|Cross Price|与 GMGN 价格做偏差校验|P01 / P03|

---

# 7. Source Capability Matrix

文件：

```text
source_capability_matrix.json
```

结构：

```json
{
  "version": "v2.0",
  "sources": {
    "gmgn": {
      "role": "token_wallet_chip_behavior_fact_source",
      "capabilities": {
        "token_profile": {
          "required": true,
          "fields": [
            "token_address",
            "chain",
            "symbol",
            "name",
            "created_at",
            "market_cap_usd",
            "liquidity_usd"
          ]
        },
        "holder_list": {
          "required": true,
          "fields": [
            "holder_address",
            "balance",
            "balance_pct",
            "rank"
          ]
        },
        "trade_events": {
          "required": true,
          "fields": [
            "wallet_address",
            "side",
            "amount_token",
            "amount_usd",
            "price_usd",
            "tx_hash",
            "timestamp"
          ]
        },
        "wallet_profile": {
          "required": false,
          "fields": [
            "wallet_address",
            "historical_win_rate",
            "historical_tokens",
            "profit_usd",
            "behavior_tags"
          ]
        }
      }
    },
    "okx": {
      "role": "quote_liquidity_execution_safety_source",
      "capabilities": {
        "quote": {
          "required": true,
          "fields": [
            "token_address",
            "chain",
            "price_usd",
            "quote_timestamp"
          ]
        },
        "liquidity": {
          "required": true,
          "fields": [
            "liquidity_usd",
            "estimated_slippage_pct",
            "depth_status"
          ]
        },
        "route": {
          "required": true,
          "fields": [
            "route_available",
            "route_source",
            "route_warning"
          ]
        },
        "security_scan": {
          "required": true,
          "fields": [
            "security_status",
            "risk_flags",
            "blocking_reason"
          ]
        }
      }
    }
  }
}
```

---

# 8. P01 核心数据模型

## 8.1 Token Fact

文件：

```text
normalized_token_fact.json
```

用途：定义 token 身份。

```json
{
  "schema_version": "v2.0",
  "token_address": {
    "value": null,
    "source": "input_or_gmgn",
    "confidence": "HIGH",
    "fetched_at": null,
    "missing_reason": null
  },
  "chain": {
    "value": "solana",
    "source": "input_or_gmgn",
    "confidence": "HIGH",
    "fetched_at": null,
    "missing_reason": null
  },
  "symbol": {
    "value": null,
    "source": "gmgn.token_profile",
    "confidence": "MEDIUM",
    "fetched_at": null,
    "missing_reason": null
  },
  "name": {
    "value": null,
    "source": "gmgn.token_profile",
    "confidence": "MEDIUM",
    "fetched_at": null,
    "missing_reason": null
  },
  "created_at": {
    "value": null,
    "source": "gmgn.token_profile",
    "confidence": "MEDIUM",
    "fetched_at": null,
    "missing_reason": null
  },
  "first_seen_at": {
    "value": null,
    "source": "system.candidate_discovery",
    "confidence": "HIGH",
    "fetched_at": null,
    "missing_reason": null
  },
  "token_age_minutes": {
    "value": null,
    "source": "derived.created_at",
    "confidence": "MEDIUM",
    "fetched_at": null,
    "missing_reason": null
  }
}
```

---

## 8.2 Market Fact

文件：

```text
normalized_market_fact.json
```

用途：定义市场事实。

```json
{
  "schema_version": "v2.0",
  "token_address": null,
  "chain": "solana",
  "price_usd": {
    "value": null,
    "primary_source": "okx.quote",
    "fallback_source": "gmgn.token_profile",
    "confidence": "HIGH",
    "age_sec": null,
    "missing_reason": null
  },
  "market_cap_usd": {
    "value": null,
    "source": "gmgn.token_profile",
    "confidence": "MEDIUM",
    "age_sec": null,
    "missing_reason": null
  },
  "discovery_market_cap_usd": {
    "value": null,
    "source": "system.first_seen_snapshot",
    "confidence": "MEDIUM",
    "age_sec": null,
    "missing_reason": null
  },
  "market_cap_change_from_discovery_pct": {
    "value": null,
    "source": "derived.current_vs_discovery",
    "confidence": "MEDIUM",
    "missing_reason": null
  },
  "liquidity_usd": {
    "value": null,
    "primary_source": "okx.liquidity",
    "fallback_source": "gmgn.token_profile",
    "confidence": "MEDIUM",
    "age_sec": null,
    "missing_reason": null
  },
  "volume_5m_usd": {
    "value": null,
    "source": "gmgn.trade_events",
    "confidence": "MEDIUM",
    "missing_reason": null
  },
  "volume_1h_usd": {
    "value": null,
    "source": "gmgn.trade_events",
    "confidence": "MEDIUM",
    "missing_reason": null
  },
  "price_cross_source_deviation_pct": {
    "value": null,
    "source": "derived.okx_vs_gmgn",
    "confidence": "HIGH",
    "missing_reason": null
  }
}
```

---

## 8.3 Wallet Fact

文件：

```text
normalized_wallet_fact.json
```

用途：定义钱包与筹码事实，不做最终行为推断。

```json
{
  "schema_version": "v2.0",
  "token_address": null,
  "chain": "solana",
  "holder_summary": {
    "holder_count": {
      "value": null,
      "source": "gmgn.holder_list",
      "confidence": "MEDIUM"
    },
    "top_10_holder_pct": {
      "value": null,
      "source": "gmgn.holder_list",
      "confidence": "MEDIUM"
    },
    "top_20_holder_pct": {
      "value": null,
      "source": "gmgn.holder_list",
      "confidence": "MEDIUM"
    },
    "fresh_wallet_holder_pct": {
      "value": null,
      "source": "derived.wallet_age",
      "confidence": "LOW"
    }
  },
  "early_wallets": [],
  "top_holders": [],
  "trade_event_summary": {
    "buy_count": null,
    "sell_count": null,
    "early_buy_count": null,
    "early_sell_count": null,
    "large_buy_count": null,
    "large_sell_count": null
  },
  "same_source_candidates": [],
  "fund_flow_edges": [],
  "data_limitations": []
}
```

注意：这里不输出“庄家意图”。它只输出事实材料。

---

## 8.4 Quote Fact

文件：

```text
normalized_quote_fact.json
```

用途：定义报价、流动性与执行可行性。

```json
{
  "schema_version": "v2.0",
  "token_address": null,
  "chain": "solana",
  "quote_status": "UNKNOWN",
  "price_usd": {
    "value": null,
    "source": "okx.quote",
    "age_sec": null,
    "confidence": "HIGH",
    "missing_reason": null
  },
  "liquidity_status": {
    "value": "UNKNOWN",
    "source": "okx.liquidity",
    "confidence": "MEDIUM",
    "missing_reason": null
  },
  "route_available": {
    "value": null,
    "source": "okx.route",
    "confidence": "MEDIUM",
    "missing_reason": null
  },
  "estimated_slippage_pct": {
    "value": null,
    "source": "okx.liquidity_or_simulator",
    "confidence": "LOW",
    "missing_reason": null
  },
  "security_status": {
    "value": "UNKNOWN",
    "source": "okx.security_scan",
    "confidence": "MEDIUM",
    "missing_reason": null
  },
  "execution_feasibility": {
    "value": "NOT_EVALUATED",
    "source": "derived.quote_liquidity_security",
    "confidence": "MEDIUM",
    "missing_reason": null
  }
}
```

---

# 9. 数据质量门设计

文件：

```text
data_quality_decision.json
```

## 9.1 质量评分维度

|维度|含义|阻断标准|
|---|---|---|
|`coverage_score`|字段完整度|强依赖字段缺失|
|`freshness_score`|数据新鲜度|报价 / 交易数据过期|
|`provenance_score`|字段来源完整度|关键字段无来源|
|`schema_validity_score`|schema 是否匹配|字段结构变化|
|`cross_source_consistency_score`|GMGN / OKX 是否冲突|价格偏差过大|
|`raw_evidence_score`|是否有 raw 证据|无 raw 禁止通过|

---

## 9.2 质量状态

```text
DATA_READY
DATA_PARTIAL_READY
DATA_PAUSE
DATA_BLOCK
DATA_SCHEMA_REVIEW
DATA_REPLAY_ONLY
```

## 9.3 状态含义

|状态|含义|下游权限|
|---|---|---|
|`DATA_READY`|数据完整、新鲜、可追溯|可进入 P02/P03/P06|
|`DATA_PARTIAL_READY`|非关键字段缺失|可观察，不可升级执行|
|`DATA_PAUSE`|关键字段暂时缺失|暂停等待下一轮|
|`DATA_BLOCK`|关键源不可用或核心字段缺失|阻断下游|
|`DATA_SCHEMA_REVIEW`|外部字段结构变化|进入合约修复|
|`DATA_REPLAY_ONLY`|只适合离线测试|禁止实时判断|

---

## 9.4 示例

```json
{
  "schema_version": "v2.0",
  "token_address": "...",
  "chain": "solana",
  "quality_scores": {
    "coverage_score": 0.84,
    "freshness_score": 0.92,
    "provenance_score": 1.0,
    "schema_validity_score": 1.0,
    "cross_source_consistency_score": 0.79,
    "raw_evidence_score": 1.0
  },
  "required_field_status": {
    "token_profile": "PRESENT",
    "holder_list": "PRESENT",
    "trade_events": "PRESENT",
    "wallet_profile": "PARTIAL",
    "quote": "PRESENT",
    "liquidity": "PRESENT",
    "security_scan": "PRESENT"
  },
  "blocking_reasons": [],
  "warnings": [
    "wallet_profile_partial",
    "gmgn_okx_price_deviation_moderate"
  ],
  "decision": "DATA_READY",
  "downstream_permissions": {
    "wallet_structure_analysis": true,
    "market_structure_analysis": true,
    "scenario_recognition": true,
    "strategy_gate": true,
    "paper_trading": true,
    "real_execution": false
  }
}
```

---

# 10. Downstream Handoff Packet

P01 最核心产物是：

```text
data_fact_handoff_packet.json
```

这是下游唯一可信入口。

```json
{
  "schema_version": "v2.0",
  "phase_id": "P01",
  "run_id": "20260513_100000",
  "token_address": "...",
  "chain": "solana",
  "data_fact_status": "DATA_READY",
  "source_health": {
    "gmgn": {
      "status": "SOURCE_READY",
      "last_checked_at": "...",
      "failure_reason": null
    },
    "okx": {
      "status": "SOURCE_READY",
      "last_checked_at": "...",
      "failure_reason": null
    }
  },
  "normalized_files": {
    "token_fact": "p01_data_fact/normalized/<token>/normalized_token_fact.json",
    "market_fact": "p01_data_fact/normalized/<token>/normalized_market_fact.json",
    "wallet_fact": "p01_data_fact/normalized/<token>/normalized_wallet_fact.json",
    "quote_fact": "p01_data_fact/normalized/<token>/normalized_quote_fact.json"
  },
  "quality_files": {
    "data_quality_decision": "p01_data_fact/quality/<token>/data_quality_decision.json",
    "coverage_report": "p01_data_fact/quality/<token>/data_coverage_report.json",
    "freshness_report": "p01_data_fact/quality/<token>/freshness_report.json",
    "provenance_report": "p01_data_fact/quality/<token>/field_provenance_report.json"
  },
  "quality_gate": {
    "decision": "DATA_READY",
    "coverage_score": 0.84,
    "freshness_score": 0.92,
    "blocking_reasons": [],
    "warnings": []
  },
  "downstream_permissions": {
    "P02_wallet_chip_structure_controller": true,
    "P03_market_structure_controller": true,
    "P04_scenario_recognition_controller": true,
    "P05_strategy_gate_controller": true,
    "P06_paper_trading_controller": true,
    "P07_real_execution_controller": false
  },
  "handoff_constraints": {
    "raw_payload_direct_access_allowed": false,
    "real_execution_allowed": false,
    "replay_only": false,
    "requires_human_review": false
  },
  "next_required_modules": [
    "P02_wallet_chip_structure_controller",
    "P03_market_structure_controller",
    "P05_strategy_gate_controller",
    "P06_paper_trading_controller"
  ]
}
```

---

# 11. P01 失败分类体系

## 11.1 数据源失败

|代码|含义|处理|
|---|---|---|
|`SOURCE_AUTH_FAILED`|权限 / key / token 问题|阻断|
|`SOURCE_NETWORK_FAILED`|网络不可达|重试 / 暂停|
|`SOURCE_TIMEOUT`|超时|重试|
|`SOURCE_RATE_LIMITED`|限流|backoff|
|`SOURCE_EMPTY_RESPONSE`|返回为空|暂停|
|`SOURCE_SCHEMA_CHANGED`|返回结构变化|schema review|
|`SOURCE_UNSUPPORTED_FIELD`|数据源不支持字段|标记限制|
|`SOURCE_UNKNOWN_ERROR`|未知异常|审计后阻断|

---

## 11.2 数据字段失败

|代码|含义|处理|
|---|---|---|
|`MISSING_REQUIRED_FIELD`|强依赖字段缺失|阻断|
|`MISSING_OPTIONAL_FIELD`|可选字段缺失|warning|
|`FIELD_TYPE_MISMATCH`|字段类型错误|schema review|
|`FIELD_OUT_OF_RANGE`|字段异常|数据质量降级|
|`FIELD_STALE`|字段过期|阻断相关下游|
|`FIELD_NO_PROVENANCE`|字段无来源|阻断|
|`FIELD_CONFLICT_BETWEEN_SOURCES`|多源冲突|降级 / 阻断|

---

## 11.3 下游权限失败

|代码|含义|处理|
|---|---|---|
|`WALLET_DATA_BLOCK`|钱包数据不足|禁止 P02|
|`MARKET_DATA_BLOCK`|市场数据不足|禁止 P03|
|`QUOTE_BLOCK`|报价不可用|禁止 P06|
|`SECURITY_UNKNOWN_PAUSE`|安全状态未知|禁止 P05/P07|
|`REPLAY_ONLY_BLOCK_REALTIME`|只允许 replay|禁止实时判断|
|`REAL_EXECUTION_DISABLED`|当前阶段禁止实盘|固定阻断|

---

# 12. P01 运行链路

```text
P01-A 阶段身份加载
  ↓
P01-B Source Registry 加载
  ↓
P01-C GMGN / OKX 连接自检
  ↓
P01-D 候选 token universe 生成
  ↓
P01-E GMGN / OKX raw 拉取
  ↓
P01-F raw manifest 写入
  ↓
P01-G normalized fact 生成
  ↓
P01-H 字段来源 / 新鲜度 / 覆盖率检查
  ↓
P01-I 跨源一致性检查
  ↓
P01-J data_quality_decision 输出
  ↓
P01-K data_fact_handoff_packet 输出
  ↓
P01-L replay fixture 更新
  ↓
P01-M audit / daily report 输出
```

---

# 13. P01 模块文件设计

## 13.1 控制器

```text
/root/sikk-gmgn/controllers/p01_data_fact_controller.py
```

职责：

```text
统一调度 P01 所有子模块。
不直接写策略。
不做交易判断。
只负责数据事实层完成度和交接包生成。
```

---

## 13.2 Connectors

```text
/root/sikk-gmgn/connectors/gmgn_connector.py
/root/sikk-gmgn/connectors/okx_connector.py
```

GMGN connector 函数：

```python
fetch_token_profile()
fetch_holder_list()
fetch_top_holders()
fetch_trade_events()
fetch_wallet_profile()
fetch_smart_money()
fetch_security()
```

OKX connector 函数：

```python
fetch_quote()
fetch_liquidity()
fetch_route()
fetch_security_scan()
```

---

## 13.3 Normalizers

```text
/root/sikk-gmgn/normalizers/p01_token_fact_normalizer.py
/root/sikk-gmgn/normalizers/p01_market_fact_normalizer.py
/root/sikk-gmgn/normalizers/p01_wallet_fact_normalizer.py
/root/sikk-gmgn/normalizers/p01_quote_fact_normalizer.py
```

职责：

```text
raw payload → normalized fact
```

每个字段必须带：

```text
value
source
fetched_at
confidence
missing_reason
```

---

## 13.4 Gates

```text
/root/sikk-gmgn/gates/p01_data_quality_gate.py
/root/sikk-gmgn/gates/p01_freshness_gate.py
/root/sikk-gmgn/gates/p01_schema_contract_gate.py
/root/sikk-gmgn/gates/p01_cross_source_consistency_gate.py
```

---

## 13.5 Contracts

```text
/root/sikk-gmgn/contracts/p01/normalized_token_fact.schema.json
/root/sikk-gmgn/contracts/p01/normalized_market_fact.schema.json
/root/sikk-gmgn/contracts/p01/normalized_wallet_fact.schema.json
/root/sikk-gmgn/contracts/p01/normalized_quote_fact.schema.json
/root/sikk-gmgn/contracts/p01/data_quality_decision.schema.json
/root/sikk-gmgn/contracts/p01/data_fact_handoff_packet.schema.json
```

---

## 13.6 Tests

```text
/root/sikk-gmgn/tests/p01/test_gmgn_connector.py
/root/sikk-gmgn/tests/p01/test_okx_connector.py
/root/sikk-gmgn/tests/p01/test_p01_data_fact_controller.py
/root/sikk-gmgn/tests/p01/test_p01_normalizers.py
/root/sikk-gmgn/tests/p01/test_p01_quality_gate.py
/root/sikk-gmgn/tests/p01/test_p01_handoff_packet.py
/root/sikk-gmgn/tests/p01/test_p01_replay_fixture.py
```

---

# 14. P01 验收标准

## 14.1 第一层验收：阶段结构成立

|项目|验收标准|
|---|---|
|阶段身份文件|yaml/md 存在|
|目录结构|p01_data_fact 完整|
|source registry|GMGN/OKX 能力矩阵存在|
|contracts|schema 文件存在|
|tests|P01 测试目录存在|

---

## 14.2 第二层验收：数据源成立

|项目|验收标准|
|---|---|
|GMGN connectivity|成功或明确失败原因|
|OKX connectivity|成功或明确失败原因|
|错误分类|不能只有 exception|
|raw 保存|每个 token 有 raw 目录|
|manifest|每个源有 fetch manifest|
|无伪造数据|不允许 synthetic payload|

---

## 14.3 第三层验收：标准化成立

|项目|验收标准|
|---|---|
|token fact|生成并通过 schema|
|market fact|生成并通过 schema|
|wallet fact|生成并通过 schema|
|quote fact|生成并通过 schema|
|missing reason|缺字段必须说明|
|provenance|关键字段必须有来源|

---

## 14.4 第四层验收：质量门成立

|项目|验收标准|
|---|---|
|coverage score|已计算|
|freshness score|已计算|
|schema validity|已检查|
|cross-source deviation|已检查|
|data_quality_decision|已生成|
|downstream permissions|已生成|

---

## 14.5 第五层验收：下游交接成立

|项目|验收标准|
|---|---|
|handoff packet|每个 token 必须生成|
|P02 权限|由 P01 控制|
|P03 权限|由 P01 控制|
|P06 权限|由 P01 控制|
|real_execution|必须 false|
|raw direct access|禁止|

---

# 15. P01 运行命令设计

```bash
cd /root/sikk-gmgn

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode init-phase

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode connectivity-check

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode build-candidate-universe \
  --limit 50

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode fetch-one \
  --token <TOKEN_ADDRESS> \
  --chain solana

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode fetch-candidates \
  --limit 20

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode normalize

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode quality-gate

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode build-handoff

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode replay \
  --fixture-dir data/gmgn_candidates_live_run/p01_data_fact/replay_fixture

pytest -q tests/p01/
```

---

# 16. P01 专业化差距审计表

当前需要 HER 审计这些问题：

|审计点|判断问题|
|---|---|
|GMGN 是否有真实 connector|如果没有，是否只有旧脚本或 skill 入口|
|OKX 是否有真实 connector|是否只能 quote，还是也能 liquidity / security|
|旧 runtime 目录是否混乱|是否存在多个数据版本|
|raw 是否保存|是否接口返回后直接被消费|
|normalized 是否统一|是否不同模块读取不同字段名|
|paper runner 数据源|是否直接读 quote/security summary|
|wallet gate 数据源|是否直接读旧 GMGN 输出|
|candidate states 数据源|是否缺少 P01 handoff|
|dashboard 数据源|是否直接读取杂乱 json|
|replay fixture 是否存在|没有则上游失败时无法调试|

---

# 17. HER 可复制执行任务书

下面是可直接发给 HER 的任务包。

```text
任务名称：
P01_data_fact_controller 专业版阶段包建设任务

任务目标：
将 SIKK Stable Trader OS 的 P01 数据事实层重建为轻量机构级事实入口控制器，使 GMGN、OKX、手动输入、历史缓存、replay fixture 等上游来源能够被统一接入、保存 raw、标准化、质量审计、输出下游交接包，并阻断所有不合格数据继续进入钱包结构、市场结构、策略门禁、纸面交易和真实执行模块。

当前背景：
系统当前跑不起来代币数据，GMGN 与 OKX 没有被正式纳入系统事实链路。请不要继续优化策略、钱包判断、paper runner、dashboard 或解释模块。当前任务只处理 P01 数据事实层。

核心定义：
P01 不是阶段说明文档，而是一个可调度阶段运行单元。它负责把上游数据源转化为可追溯、可审计、可质量判断、可交接给下游的标准事实数据包。

硬规则：
1. 所有 GMGN / OKX 返回必须先保存 raw。
2. 下游模块不得直接读取 raw payload。
3. 下游模块只能读取 normalized fact 与 data_fact_handoff_packet。
4. 数据缺失必须状态化，不允许静默忽略。
5. 字段来源必须记录 provenance。
6. 报价、交易、钱包数据必须检查 freshness。
7. schema 变化必须进入 DATA_SCHEMA_REVIEW。
8. 不允许伪造数据。
9. replay fixture 必须标记 DATA_REPLAY_ONLY。
10. P01 阶段 real_execution 必须永久 false。

需要建立目录：
/root/sikk-gmgn/data/gmgn_candidates_live_run/p01_data_fact/

需要建立子目录：
phase_identity/
source_registry/
connectivity/
candidate_universe/
raw/gmgn/
raw/okx/
normalized/
quality/
handoff/
replay_fixture/
audit/
reports/

需要建立代码文件：
/root/sikk-gmgn/controllers/p01_data_fact_controller.py
/root/sikk-gmgn/connectors/gmgn_connector.py
/root/sikk-gmgn/connectors/okx_connector.py
/root/sikk-gmgn/normalizers/p01_token_fact_normalizer.py
/root/sikk-gmgn/normalizers/p01_market_fact_normalizer.py
/root/sikk-gmgn/normalizers/p01_wallet_fact_normalizer.py
/root/sikk-gmgn/normalizers/p01_quote_fact_normalizer.py
/root/sikk-gmgn/gates/p01_data_quality_gate.py
/root/sikk-gmgn/gates/p01_freshness_gate.py
/root/sikk-gmgn/gates/p01_schema_contract_gate.py
/root/sikk-gmgn/gates/p01_cross_source_consistency_gate.py

需要建立 contracts：
/root/sikk-gmgn/contracts/p01/normalized_token_fact.schema.json
/root/sikk-gmgn/contracts/p01/normalized_market_fact.schema.json
/root/sikk-gmgn/contracts/p01/normalized_wallet_fact.schema.json
/root/sikk-gmgn/contracts/p01/normalized_quote_fact.schema.json
/root/sikk-gmgn/contracts/p01/data_quality_decision.schema.json
/root/sikk-gmgn/contracts/p01/data_fact_handoff_packet.schema.json

需要建立测试：
/root/sikk-gmgn/tests/p01/test_gmgn_connector.py
/root/sikk-gmgn/tests/p01/test_okx_connector.py
/root/sikk-gmgn/tests/p01/test_p01_data_fact_controller.py
/root/sikk-gmgn/tests/p01/test_p01_normalizers.py
/root/sikk-gmgn/tests/p01/test_p01_quality_gate.py
/root/sikk-gmgn/tests/p01/test_p01_handoff_packet.py
/root/sikk-gmgn/tests/p01/test_p01_replay_fixture.py

第一步：阶段身份文件
创建：
- phase_01_data_fact_controller.yaml
- phase_01_data_fact_controller.md

必须写明：
- P01 负责什么
- P01 不负责什么
- 上游来源
- 下游消费者
- 核心输出
- 硬规则
- 状态码
- 失败策略

第二步：Source Registry
创建：
- gmgn_source_profile.yaml
- okx_source_profile.yaml
- manual_input_source_profile.yaml
- local_cache_source_profile.yaml
- source_capability_matrix.json

必须定义：
GMGN 是 Token + Wallet + Chip + Behavior Fact Source。
OKX 是 Quote + Liquidity + Execution Feasibility + Safety Cross-check Source。

第三步：Connectivity Check
实现：
python3 controllers/p01_data_fact_controller.py --mode connectivity-check

输出：
- gmgn_connectivity_report.json
- okx_connectivity_report.json
- source_health_summary.json

失败必须分类：
- SOURCE_AUTH_FAILED
- SOURCE_NETWORK_FAILED
- SOURCE_TIMEOUT
- SOURCE_RATE_LIMITED
- SOURCE_EMPTY_RESPONSE
- SOURCE_SCHEMA_CHANGED
- SOURCE_UNKNOWN_ERROR

第四步：Candidate Universe
实现候选 token 统一入口。

输出：
- candidate_token_universe.json
- candidate_token_universe.csv
- candidate_token_universe.md
- candidate_source_trace.jsonl

候选来源包括：
- GMGN 新币
- GMGN 热门币
- 钱包关联 token
- 手动输入 token
- local cache
- replay fixture

第五步：Raw Ingestion
所有数据必须先保存 raw。

GMGN raw：
- token_profile_raw.json
- holder_list_raw.json
- top_holders_raw.json
- trade_events_raw.json
- wallet_profile_raw.json
- smart_money_raw.json
- security_raw.json
- gmgn_fetch_manifest.json

OKX raw：
- quote_raw.json
- liquidity_raw.json
- route_raw.json
- security_scan_raw.json
- okx_fetch_manifest.json

如果实际接口无法提供某些字段，不允许伪造。必须写入：
MISSING_WITH_SOURCE_LIMITATION

第六步：Normalization
将 raw 转成：
- normalized_token_fact.json
- normalized_market_fact.json
- normalized_wallet_fact.json
- normalized_quote_fact.json

每个字段必须包含：
- value
- source
- fetched_at
- confidence
- missing_reason

第七步：Quality Gate
生成：
- data_coverage_report.json
- freshness_report.json
- field_provenance_report.json
- schema_validation_report.json
- cross_source_consistency_report.json
- data_quality_decision.json

data_quality_decision 只能输出：
- DATA_READY
- DATA_PARTIAL_READY
- DATA_PAUSE
- DATA_BLOCK
- DATA_SCHEMA_REVIEW
- DATA_REPLAY_ONLY

第八步：Handoff Packet
生成：
- data_fact_handoff_packet.json
- downstream_readiness_report.md
- downstream_permission_matrix.json

handoff 必须包含：
- run_id
- token_address
- chain
- data_fact_status
- source_health
- normalized_files
- quality_files
- quality_gate
- downstream_permissions
- handoff_constraints
- next_required_modules

downstream_permissions 必须至少包含：
- P02_wallet_chip_structure_controller
- P03_market_structure_controller
- P04_scenario_recognition_controller
- P05_strategy_gate_controller
- P06_paper_trading_controller
- P07_real_execution_controller

其中 P07_real_execution_controller 必须固定 false。

第九步：Replay Fixture
保存至少 3 个 token 的完整样本：
- raw
- normalized
- quality
- handoff

输出：
- fixture_manifest.json
- replay_validation_report.json

replay 数据只能用于测试，不能作为实时交易判断。

第十步：Runtime Audit
生成：
- data_source_runtime_log.jsonl
- source_error_events.jsonl
- data_quality_events.jsonl
- p01_phase_status.json
- daily_data_source_report.md
- p01_completion_report.md
- p01_gap_audit_report.md

日报必须说明：
- 本轮处理 token 数
- GMGN 成功 / 失败数量
- OKX 成功 / 失败数量
- DATA_READY 数量
- DATA_BLOCK 数量
- DATA_PAUSE 数量
- DATA_SCHEMA_REVIEW 数量
- 最常见失败原因
- 是否允许 P02/P03/P06 继续运行

验收命令：
cd /root/sikk-gmgn

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode init-phase

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode connectivity-check

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode build-candidate-universe \
  --limit 50

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode fetch-candidates \
  --limit 20

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode normalize

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode quality-gate

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode build-handoff

python3 controllers/p01_data_fact_controller.py \
  --run-dir data/gmgn_candidates_live_run \
  --mode replay \
  --fixture-dir data/gmgn_candidates_live_run/p01_data_fact/replay_fixture

pytest -q tests/p01/

最终验收标准：
1. P01 阶段身份文件存在。
2. source registry 完整。
3. GMGN / OKX connectivity report 存在。
4. source_health_summary.json 存在。
5. 每个 token 都有 raw 或明确失败原因。
6. 每个 token 都有 normalized fact 或明确失败原因。
7. 每个 token 都有 data_quality_decision。
8. 每个 token 都有 data_fact_handoff_packet。
9. 缺失字段必须有 missing_reason。
10. 关键字段必须有 provenance。
11. replay fixture 至少包含 3 个 token。
12. 所有 P01 测试通过。
13. real_execution 必须 false。
14. 下游不得直接读取 GMGN / OKX raw。
15. 输出 p01_completion_report.md 和 p01_gap_audit_report.md。
```

---

# 18. P01 完成后的系统状态

完成后，系统状态应从：

```text
P01_DATA_FACT_LAYER_INCOMPLETE
```

升级为：

```text
P01_DATA_FACT_LAYER_READY
```

或者：

```text
P01_READY_WITH_WARNINGS
```

只有达到这一步，才允许进入：

```text
P02 钱包 / 筹码结构层
P03 市场结构层
P04 场景识别层
P05 策略门禁层
P06 纸面交易层
```

---

# 19. 不应继续做的事情

在 P01 没完成之前，不建议继续推进：

```text
钱包角色最终分类
主导侧生命周期推断
策略信号优化
纸面交易收益统计
Telegram 面板美化
dashboard 展示层
解释模块扩写
真实交易门禁
```

原因：

```text
事实层不成立，所有下游判断都会变成基于不完整数据的解释污染。
```

---

# 20. 本次认知升级点

1. **P01 不是数据文档，而是事实入口控制器。**
2. **GMGN / OKX 接入属于 P01 核心成立条件。**
3. **P01 的核心产物不是 raw 数据，而是 `data_fact_handoff_packet.json`。**
4. **下游必须被 P01 授权读取，不能各自乱读接口输出。**
5. **缺字段、旧字段、空返回、接口失败都必须状态化。**
6. **专业化不是把模块堆多，而是每个字段都有来源、时间、置信度、缺失原因、下游权限。**
7. **P01 完成前，策略层继续优化没有意义。**

---

# 21. 尚未解决问题

1. GMGN 当前到底通过什么方式接入：skill、接口、脚本、本地缓存，仍需 HER 审计。
2. OKX 当前 connector 是否已经存在，还是只有 quote/security summary，需要检查。
3. 旧目录 `data/gmgn_candidates_live_run/` 中哪些文件可复用，哪些属于历史混乱输出，需要迁移映射。
4. 当前 paper runner 是否直接读取旧 quote/security summary，需要改为读取 P01 handoff。
5. 当前 wallet gate 是否直接读取 GMGN 原始输出，需要改为读取 normalized wallet fact。
6. replay fixture 需要至少 3 个真实 token 样本，否则上游失败时无法离线验证 P01。
7. P01 完成后，需要立刻设计 P02 如何读取 `data_fact_handoff_packet.json`，而不是重新发明数据入口。