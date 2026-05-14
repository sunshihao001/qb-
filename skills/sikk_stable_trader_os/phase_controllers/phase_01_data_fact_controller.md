# Phase 01：数据事实层 Controller

## 0. 文档状态

```text
文档类型：阶段信息文档 / Phase Controller
当前状态：专业化设计 v1.0
是否正式 Skill：否
是否允许直接交易判断：否
是否允许输出买卖建议：否
下一步：用真实样本验证字段来源与输出合约
```

本阶段是 SIKK Stable Trader OS 的第一道事实闸门。它不判断涨跌，不判断是否参与，不判断结构角色，只负责把 GMGN / OKX / RPC / K 线 / quote / 钱包快照等原始输入变成可被下游读取、可审计、可复盘的事实包。

## 1. 阶段定位

### 本阶段负责回答

```text
当前 token 的基础事实数据是否足够、是否新鲜、是否字段完整、是否时间口径一致、是否可以交给下一阶段继续判断？
```

### 本阶段不负责回答

- 不判断是否买入。
- 不判断是否卖出。
- 不判断“确定庄家”。
- 不判断 A+P1。
- 不判断钱包是否为主力。
- 不判断当前是否已经完成 AVWAP / POC / Failure Test。
- 不做资金路径归因结论。
- 不做策略门禁结论。

本阶段只能输出数据质量状态：

```text
DATA_OK
DATA_WEAK
DATA_INVALID
```

## 2. 输入数据

### 2.1 标准输入根目录

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/
```

### 2.2 允许输入文件

优先读取：

```text
wallet_data/raw/gmgn_wallet_rows_raw.json
wallet_data/raw/gmgn_wallet_trade_input.json
wallet_data/raw/gmgn_wallet_profile_input.json
wallet_data/raw/okx_token_snapshot_raw.json
wallet_data/raw/rpc_token_snapshot_raw.json
wallet_data/raw/kline_snapshot_raw.json
wallet_data/raw/quote_snapshot_raw.json
manifest/token_output_manifest.json
```

如果标准文件不存在，可以读取 legacy fallback，但必须在 audit 中写明：

```text
fallback_used: true
fallback_source: <path>
fallback_reason: <reason>
```

### 2.3 必需字段

基础 token 字段：

- `token_address`：string，必填，来自用户输入或 manifest。
- `chain`：string，必填，默认 Solana 时必须明确写 `solana`。
- `mode`：string，必填，取值 `live` / `replay` / `import` / `manual`。
- `snapshot_timestamp`：datetime，必填，原始快照采集时间。
- `source_name`：string，必填，例如 `gmgn` / `okx` / `rpc` / `quote`。
- `source_file`：string，必填，原始文件路径。

GMGN 钱包行字段：

- `wallet_address`：string，钱包地址。
- `first_seen_time`：datetime，首次出现时间。
- `buy_time`：datetime，可缺失但必须标记。
- `sell_time`：datetime，可缺失但必须标记。
- `buy_amount`：number，可缺失。
- `sell_amount`：number，可缺失。
- `realized_profit`：number，可缺失。
- `unrealized_profit`：number，可缺失。
- `holding_amount`：number，可缺失。
- `holding_ratio`：number，可缺失。
- `gmgn_tag`：string，可缺失。

K 线 / 市场字段：

- `open_time`：datetime。
- `close_time`：datetime。
- `open`：number。
- `high`：number。
- `low`：number。
- `close`：number。
- `volume`：number。
- `liquidity`：number，可缺失。
- `market_cap`：number，可缺失。

Quote / 安全字段：

- `price`：number。
- `price_impact`：number，可缺失。
- `slippage_estimate`：number，可缺失。
- `liquidity_usd`：number，可缺失。
- `security_flags`：array，可缺失但必须标记。

### 2.4 缺失字段处理

禁止用空字符串、0、false 伪装缺失。

统一写入：

```json
{
  "field": "buy_time",
  "status": "missing",
  "source_file": "wallet_data/raw/gmgn_wallet_rows_raw.json",
  "impact": "cannot measure early-window timing precisely"
}
```

## 3. 核心判断对象

本阶段只判断数据质量，不判断交易方向。

核心判断对象：

1. 数据是否存在。
2. 必需字段是否完整。
3. 字段类型是否正确。
4. 时间口径是否一致。
5. 快照是否过期。
6. 多源字段是否冲突。
7. 是否存在污染路径。
8. 是否能生成下游 handoff。

## 4. 判断规则

### 4.1 正向证据

可支持 `DATA_OK` 的证据：

- 标准输入目录存在。
- manifest 存在且 token_address / mode / source_files 可读。
- GMGN 钱包原始行存在。
- 关键字段缺失率低于阶段阈值。
- 快照时间在允许窗口内。
- K 线时间范围覆盖结构判断所需窗口。
- quote / liquidity 数据存在或明确标记为可选缺口。
- 无跨 token 混入。
- 可生成标准 normalized / summary / handoff 文件。

### 4.2 反向证据

导致 `DATA_WEAK` 的证据：

- 部分可选字段缺失。
- GMGN tag 缺失但钱包地址和交易字段存在。
- quote 数据缺失但本轮只做结构事实预处理。
- K 线窗口不足但仍有基础价格序列。
- 多源字段轻微冲突但不影响 token 身份和主时间轴。
- 采集时间略旧，需要下游降置信。

### 4.3 一票否决 / 硬否决

直接导致 `DATA_INVALID`：

- token_address 缺失或格式明显错误。
- source_file 不存在。
- manifest 指向的 token 与当前 token 不一致。
- raw 文件为空或无法解析。
- 必需字段大面积缺失，无法构建事实表。
- 时间字段无法解析，无法建立主时间轴。
- 发现跨 token 数据混入且不能隔离。
- 输入来自禁止写入或污染目录，且无法证明来源。

### 4.4 不足以判断条件

以下情况不得升级为 `DATA_OK`：

- 只有截图或自然语言描述。
- 只有报告，没有原始数据。
- 只有 dashboard 输出，没有 manifest。
- 只有下游推断，没有 source_refs。
- 只有旧目录数据但无法映射字段来源。

## 5. 输出文件

### 5.1 标准输出目录

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/wallet_data/summary/
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/wallet_data/normalized/
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/structure_analysis/handoff/
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/structure_analysis/reports/
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/manifest/
```

### 5.2 必须生成的输出

```text
wallet_data/summary/data_quality_summary.json
wallet_data/summary/missing_fields_report.json
wallet_data/summary/time_validity_report.json
wallet_data/normalized/wallet_trade_normalized.json
wallet_data/normalized/kline_normalized.json
structure_analysis/handoff/phase_01_handoff_packet.json
structure_analysis/reports/phase_01_data_fact_audit.md
manifest/field_source_registry.json
```

## 6. 输出字段

### 6.1 data_quality_summary.json

```json
{
  "token_address": "<token>",
  "chain": "solana",
  "mode": "live|replay|import|manual",
  "phase": "phase_01_data_fact",
  "status_code": "DATA_OK|DATA_WEAK|DATA_INVALID",
  "data_quality_score": 0.0,
  "snapshot_timestamp": "ISO-8601",
  "freshness_status": "fresh|stale|unknown",
  "required_fields_total": 0,
  "required_fields_missing": 0,
  "optional_fields_missing": 0,
  "source_files": [],
  "fallback_used": false,
  "positive_evidence": [],
  "negative_evidence": [],
  "counter_evidence": [],
  "hard_negative_trigger": null,
  "missing_fields": [],
  "gaps": [],
  "invalidation_condition": [],
  "confidence_level": "high|medium|low",
  "handoff_target": "phase_02_multi_model_scene_recognition",
  "audit_refs": [],
  "source_refs": []
}
```

### 6.2 phase_01_handoff_packet.json

```json
{
  "from_phase": "phase_01_data_fact",
  "to_phase": "phase_02_multi_model_scene_recognition",
  "handoff_status": "ALLOW|PAUSE|BLOCK",
  "status_code": "DATA_OK|DATA_WEAK|DATA_INVALID",
  "readable_outputs": {
    "data_quality_summary": "wallet_data/summary/data_quality_summary.json",
    "wallet_trade_normalized": "wallet_data/normalized/wallet_trade_normalized.json",
    "kline_normalized": "wallet_data/normalized/kline_normalized.json",
    "field_source_registry": "manifest/field_source_registry.json"
  },
  "downstream_warnings": [],
  "missing_fields": [],
  "gaps": [],
  "audit_refs": []
}
```

## 7. 下游交接

### 7.1 交给哪个阶段

默认交给：

```text
phase_02_multi_model_scene_recognition
```

兼容旧体系时可映射到：

```text
phase_02_wallet_structure_layer
```

### 7.2 下游必须读取字段

- `status_code`
- `data_quality_score`
- `freshness_status`
- `source_files`
- `field_source_registry`
- `missing_fields`
- `gaps`
- `wallet_trade_normalized`
- `kline_normalized`
- `audit_refs`

### 7.3 只作为报告字段

- `summary_text`
- `operator_notes`
- `human_review_notes`

## 8. 验收标准

阶段完成必须同时满足：

- 标准输出文件已生成。
- 必需字段有明确存在 / missing 状态。
- 每个输出字段有来源文件或系统推导说明。
- 存在 `positive_evidence`。
- 存在 `negative_evidence` 或明确为空数组并说明无反证。
- 存在 `counter_evidence` 或明确为空数组并说明无反证。
- 硬否决检查已运行。
- `DATA_INVALID` 时必须阻断下游。
- `DATA_WEAK` 时只能允许下游降置信读取，不能强通过。
- handoff 文件存在。
- audit 文件存在。
- HER 可按路径自动读取。

## 9. 失败处理

### 9.1 数据缺失

写入 `missing_fields_report.json`，状态降级为 `DATA_WEAK` 或 `DATA_INVALID`。

### 9.2 字段冲突

写入 `gaps`：

```json
{
  "field": "market_cap",
  "sources": ["gmgn", "okx"],
  "conflict": "values diverge beyond threshold",
  "resolution": "prefer source priority or mark unresolved"
}
```

### 9.3 判断不足

禁止输出自然语言通过。必须输出：

```text
DATA_WEAK
```

或：

```text
DATA_INVALID
```

### 9.4 是否允许进入下一阶段

```text
DATA_OK      -> ALLOW
DATA_WEAK    -> PAUSE / ALLOW_WITH_LOW_CONFIDENCE
DATA_INVALID -> BLOCK
```

## 10. 示例输出

### 10.1 data_quality_summary.json 示例

```json
{
  "token_address": "So11111111111111111111111111111111111111112",
  "chain": "solana",
  "mode": "replay",
  "phase": "phase_01_data_fact",
  "status_code": "DATA_WEAK",
  "data_quality_score": 0.72,
  "snapshot_timestamp": "2026-05-09T00:00:00Z",
  "freshness_status": "stale",
  "required_fields_total": 18,
  "required_fields_missing": 2,
  "optional_fields_missing": 5,
  "source_files": [
    "wallet_data/raw/gmgn_wallet_rows_raw.json",
    "wallet_data/raw/kline_snapshot_raw.json"
  ],
  "fallback_used": false,
  "positive_evidence": [
    "GMGN wallet rows parsed",
    "kline snapshot parsed"
  ],
  "negative_evidence": [
    "quote snapshot missing"
  ],
  "counter_evidence": [
    "freshness stale; live decision prohibited"
  ],
  "hard_negative_trigger": null,
  "missing_fields": [
    {
      "field": "quote_snapshot_raw.json",
      "status": "missing",
      "impact": "execution risk cannot be evaluated"
    }
  ],
  "gaps": [],
  "invalidation_condition": [],
  "confidence_level": "medium",
  "handoff_target": "phase_02_multi_model_scene_recognition",
  "audit_refs": [
    "structure_analysis/reports/phase_01_data_fact_audit.md"
  ],
  "source_refs": [
    "manifest/field_source_registry.json"
  ]
}
```

## 11. 接入点

当前文档是阶段信息文档。后续代码接入点应为：

```text
modules/runtime/contract_validator.py
modules/runtime/phase_runner.py
modules/source_wallet_bot/path_resolver.py
modules/source_wallet_bot/field_source_registry.py
modules/source_wallet_bot/data_quality_checker.py
```

CLI 入口候选：

```text
python3 tools/run_phase.py --phase phase_01_data_fact --mode <mode> --token <token_address>
python3 tools/validate_contract.py --contract contracts/phase_01_data_fact/input_contract.json --input <input.json>
```

## 12. 待补 gaps

```text
gaps:
- GMGN 原始字段名到标准字段名的完整映射表待补。
- OKX token snapshot 原始字段待绑定。
- RPC token snapshot 原始字段待绑定。
- K 线采样窗口和 freshness 阈值待量化。
- data_quality_score 评分公式待用样本校准。
- DATA_WEAK 是否允许下游读取的细分规则待回放验证。
```
