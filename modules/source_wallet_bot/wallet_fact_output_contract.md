# wallet_fact 标准输出合同

## 合同目标

把 Source Wallet Bot 的分散事实输出，统一组织成 Intel Bot 更容易消费的 `wallet_fact` 包。

## 输入

允许输入：

- L0 链上 DEX swap / transfer
- L1 GMGN holders / traders / wallet trade / trader detail
- L1 OKX quote / scan，只用于 quote/security/liquidity 类
- L2 Source Wallet Bot normalized 产物

禁止输入：

- dashboard 反推字段
- paper runner 反推字段
- report 反推字段
- case file 反推字段

## 输出文件

### 1. wallet_structure_normalized.json

每个钱包一行，聚合 class 4 + class 8 + role decision。

必须包含：

- token_address
- wallet_address
- snapshot_time
- source_name
- retrieved_at
- normalized_at
- first_buy_time
- buy_amount_total
- sell_amount_total
- current_balance
- holding_ratio
- exit_ratio
- realized_profit
- unrealized_profit
- pnl_multiple
- gmgn_tags
- is_fresh_wallet
- is_old_wallet
- is_sniper
- is_bundle
- is_insider
- is_whale
- role_candidates
- evidence_level
- risk_level
- data_quality_score

### 2. chip_distribution_summary.json

Token 级筹码摘要。

必须包含：

- token_address
- snapshot_time
- wallet_count
- holder_count
- total_current_balance
- full_exit_wallet_count
- partial_exit_wallet_count
- same_source_group_count
- same_source_group_wallet_count
- result_wallet_candidate_count
- counterparty_whale_candidate_count
- structure_wallet_candidate_count
- top_wallet_balance
- top10_wallet_balance_sum
- top10_wallet_balance_pct_of_tracked
- chip_concentration_level
- chip_transfer_status
- data_quality_score

### 3. same_source_groups.json

Intel Bot 可读的同源组视图。

必须包含：

- token_address
- group_id
- source_address
- member_count
- member_addresses
- evidence_level
- risk_level
- group_confidence
- evidence_basis

### 4. fund_flow_edges.csv

资金边表。

必须包含：

- token_address
- from_address
- to_address
- asset
- amount
- transfer_time
- relation_type
- source_type
- confidence_score
- evidence_note

### 5. address_history.json

历史地址库入口。当前 live 单 token 阶段先输出本 token 的地址 persona seed。

必须包含：

- wallet_address
- appeared_token_count
- appeared_tokens
- role_history
- profitable_token_count
- losing_token_count
- avg_roi
- max_roi
- repeated_source_addresses
- repeated_backflow_addresses
- current_persona
- evidence_score
- risk_score
- tracking_level
- last_seen_time

### 6. wallet_fact_report.md

给人看的结构化摘要，不逐钱包展开，只输出聚合统计、风险集中点、字段缺口和需要补查。

### 7. wallet_fact_package_manifest.json

包 manifest：列出输入、输出、source level、安全边界、生成时间、record_count。

## 输出语言约束

允许：

- 疑似结构执行钱包
- 疑似同源执行组
- 疑似分发接收钱包
- 疑似派发钱包
- 疑似利润回收钱包
- 疑似核心资金源候选
- 疑似接盘鲸鱼
- 疑似结果钱包
- 证据不足
- 字段缺失
## Forbidden phrase policy

以下为禁止输出类别，文档与代码中应避免写出原始禁用短语；统一使用：`禁止绝对化庄家/内幕/老鼠仓表述`。
- trade_allowed
- buy_signal
- sell_signal
- execute_now
- PAPER_READY
- BLOCKED
