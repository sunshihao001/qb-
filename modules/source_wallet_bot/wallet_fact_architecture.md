# wallet_fact 专业化体系重构方案

## 触发原因

用户反馈：`wallet_fact/模块感觉还是不成体系，没有之前的好`。

本轮修正目标：把当前 Source Wallet Bot 中相对分散的 normalizer / classifier / handoff 输出，重组为一个更像旧 wallet_fact 的体系化事实模块，同时保留已经建立的 Source Bot 安全边界。

## 定位

`wallet_fact` 不是单个 normalizer，而是钱包事实与筹码事实的上游证据层。

它应该按“数据类别 → 标准产物 → 汇总视图 → 下游 handoff”的方式组织。

## 总体结构

```text
wallet_fact/
├── class_04_wallet_trade/
├── class_05_token_transfer_source/
├── class_06_funding_source/
├── class_07_backflow/
├── class_08_gmgn_wallet_profile/
├── class_09_same_source_evidence/
├── class_10_snapshot_delta/
├── class_11_quote_security/
├── aggregate_outputs/
├── reports/
└── handoff/
```

在当前项目中落地为：

```text
modules/source_wallet_bot/wallet_fact_architecture.md
modules/source_wallet_bot/wallet_fact_output_contract.md
modules/source_wallet_bot/wallet_fact_schema_index.json
modules/source_wallet_bot/wallet_fact_builder.py
```

## 标准类别

### Class 4 — 钱包交易数据

输出：

```text
wallet_trade_normalized.json
```

用途：

- 单钱包成本
- 同源组成本
- 派发进度
- 疑似结果钱包
- 疑似接盘鲸鱼

### Class 5 — Token 转账 / Token 来源

输出：

```text
token_transfer_normalized.json
token_source_classification_base.json
```

用途：

- 区分主动买入、Token 转入、分发接收、空投接收、来源未知
- 防止把 transfer-in 当成真实买入成本

### Class 6 — 资金来源

输出：

```text
funding_flow_normalized.json
funding_source_normalized.json
```

用途：

- 买入前 SOL / USDC 来源
- 疑似同源资金组
- 疑似核心资金源候选

### Class 7 — 卖后回流

输出：

```text
backflow_paths_normalized.json
```

用途：

- 疑似利润回收钱包
- 疑似核心回流节点
- 同源证据升级

### Class 8 — GMGN 标签 / 钱包画像

输出：

```text
gmgn_wallet_tags_normalized.json
wallet_profile_normalized.json
```

用途：

- GMGN 标签强 hint
- fresh / sniper / bundle / insider / whale
- 疑似结构执行钱包触发

### Class 9 — 同源证据底座

输出：

```text
same_source_evidence_normalized.json
```

用途：

- by_funding_source
- by_backflow_address
- by_path_signature
- by_gmgn_tag_set

### Class 10 — 多快照 delta

输出：

```text
wallet_snapshot_delta_source.json
holder_delta_normalized.json
```

用途：

- 持仓变化
- 派发进度变化
- 同源组剩余筹码变化

### Class 11 — 报价 / 安全 / 流动性

输出：

```text
quote_security_normalized.json
```

用途：

- 当前持仓条件背景
- liquidity / slippage / security flags
- 不输出交易许可

## 聚合输出

为恢复旧 wallet_fact 的体系感，新增聚合视图：

```text
wallet_structure_normalized.json
chip_distribution_summary.json
same_source_groups.json
fund_flow_edges.csv
address_history.json
wallet_fact_report.md
wallet_fact_package_manifest.json
```

## 与现有 Source Wallet Bot 的关系

现有文件继续保留：

- `wallet_trade_normalized.json`
- `wallet_entity_profile_normalized.json`
- `same_source_evidence_normalized.json`
- `wallet_intelligence_decision.json`
- `bot2_handoff_packet.json`

新增 wallet_fact builder 负责把它们组合为更体系化的 wallet_fact 输出。

## 安全边界

仍然禁止：

- 状态机
- paper runner
- 实盘执行
- 私钥
- 签名
- 广播
- swap
- 确定性庄家 / 内幕判断

## `.gz` 文件说明

Telegram / 文档解析器不支持 `.gz`。处理 `.gz` 应走文件系统或终端解压 / 检查流程，不能直接当文档上传解析。

建议：

```bash
gzip -l file.gz
gzip -dc file.gz > imports/staging/<safe_name>.jsonl
```

只写 staging，不覆盖 runtime。
