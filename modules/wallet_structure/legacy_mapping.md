# 旧 SIKK-GMGN 单币钱包报告脚本映射

## 旧脚本功能清单

源文件：`sikk_gmgn_token_report.py`

旧脚本本质是“单币钱包结构采集报告器”，不是独立模块。它完成以下动作：

1. 接收 Solana `token_address`。
2. 调用 `gmgn-cli` 拉取 token 基础信息、安全信息、池子信息、1m K 线。
3. 调用多个 GMGN 钱包列表接口，分别拉取 top holder、盈利交易者、smart、bundler、transfer_in、renowned、fresh、rat。
4. 按钱包地址合并列表，保留 `source_lists`。
5. 使用 `classify(w)` 基于浅层 GMGN 字段与少量转入字段做角色初判。
6. 输出 8 个分析 CSV。
7. 复制 3 个 canonical CSV 文件名作为导入层：`sikk_gmgn_master_log.csv`、`infrastructure_registry.csv`、`review_update_history.csv`。
8. 生成 `sikk_gmgn_report.md`。
9. 将 CSV/Markdown 打包成 zip。

## 旧 gmgn-cli 调用清单

- `gmgn-cli token info --chain sol --address <token> --raw`
- `gmgn-cli token security --chain sol --address <token> --raw`
- `gmgn-cli token pool --chain sol --address <token> --raw`
- `gmgn-cli market kline --chain sol --address <token> --resolution 1m --from <now-3600> --to <now> --raw`
- `gmgn-cli token holders --chain sol --address <token> --limit 20 --order-by amount_percentage --direction desc --raw`
- `gmgn-cli token traders --chain sol --address <token> --limit 15 --order-by profit --direction desc --raw`
- `gmgn-cli token holders --chain sol --address <token> --limit 10 --tag smart_degen --order-by amount_percentage --direction desc --raw`
- `gmgn-cli token holders --chain sol --address <token> --limit 10 --tag bundler --order-by amount_percentage --direction desc --raw`
- `gmgn-cli token holders --chain sol --address <token> --limit 10 --tag transfer_in --order-by amount_percentage --direction desc --raw`
- `gmgn-cli token holders --chain sol --address <token> --limit 8 --tag renowned --order-by amount_percentage --direction desc --raw`
- `gmgn-cli token holders --chain sol --address <token> --limit 8 --tag fresh_wallet --order-by amount_percentage --direction desc --raw`
- `gmgn-cli token holders --chain sol --address <token> --limit 8 --tag rat_trader --order-by amount_percentage --direction desc --raw`

## 旧输出文件清单

- `01_analysis_depth.csv`：根据流动性、bundler、fresh、sniper、smart、Top10 等判断分析深度。
- `02_token_basic.csv`：代币基础资料、价格、市值、流动性、创建时间、主池和链接字段。
- `03_structure_metrics.csv`：权限、安全、筹码集中、GMGN 标签统计和 1h K 线摘要。
- `04_key_address_matrix.csv`：旧系统核心钱包矩阵，包含标签、角色、持仓、买卖、利润、来源、动作、复盘建议。
- `05_infrastructure_registry.csv`：LP/Pool 和 native funding source 候选的基础设施登记。
- `06_low_weight_scope.csv`：低权重地址范围与跳过深挖原因。
- `07_review_plan.csv`：T+1h/T+6h/T+24h/T+72h/T+7d 复盘计划。
- `08_summary.csv`：代币总体等级、正向/风险信号、输出目录。
- `sikk_gmgn_master_log.csv`：`04_key_address_matrix.csv` 的 canonical 复制。
- `infrastructure_registry.csv`：`05_infrastructure_registry.csv` 的 canonical 复制。
- `review_update_history.csv`：`07_review_plan.csv` 的 canonical 复制。
- `sikk_gmgn_report.md`：人类可读报告摘要。

## 旧字段清单

旧脚本直接或间接使用字段包括：

- token 层：`symbol`、`name`、`price`、`circulating_supply`、`liquidity`、`creation_timestamp`、`open_timestamp`、`launchpad_platform`、`biggest_pool_address`、`link.gmgn`。
- security/stat 层：`renounced_mint`、`renounced_freeze_account`、`buy_tax`、`sell_tax`、`burn_status`、`top_10_holder_rate`、`top_bundler_trader_percentage`、`fresh_wallet_rate`、`top_rat_trader_percentage`、`top_entrapment_trader_percentage`、`bot_degen_rate`。
- wallet tag 层：`tags`、`maker_token_tags`、`smart_degen`、`bundler`、`kol`、`top_holder`、`fresh_wallet`、`rat_trader`。
- wallet behavior 层：`amount_percentage`、`usd_value`、`sell_amount_percentage`、`profit`、`total_profit`、`pnl`、`buy_volume_cur`、`buy_volume_usd`、`total_buy_usd`、`sell_volume_cur`、`sell_volume_usd`、`total_sell_usd`、`buy_count`、`sell_count`、`realized_profit`、`unrealized_profit`、`profit_percentage`、`roi`。
- source 层：`transfer_in`、`token_transfer_in.address`、`native_transfer.from_address`、`token_transfer_out`、`funding_source`。
- activity 层：`start_holding_at`、`first_buy_timestamp`、`created_at`、`last_active_timestamp`、`last_active_time`。

## 旧分类规则清单

旧 `classify(w)` 规则如下：

1. `addr_type == 2` → LP池子，I1，基础设施排除。
2. `rat_trader` in `maker_token_tags` → 可疑中转节点，R2。
3. `transfer_in` 且 `sell_amount_percentage >= 0.6` → 分发派发钱包，E4/R2。
4. `transfer_in` → 分发接收钱包，E3/E4。
5. `smart_degen` 且 `profit > 1000` → 结果钱包，E4。
6. `sell_amount_percentage >= 0.6` 且 `buy_volume > 10000` → 接盘鲸鱼，R2。
7. `bundler` 且 `profit > 5000` → 结果钱包，E4。
8. `is_new` 且 `bundler` → 新钱包狙击，E3。
9. `kol` → 结果钱包，E3/R1。
10. `holding_pct > 1%` 或 `top_holder` → 普通交易钱包，E2。
11. 默认 → 普通交易钱包，E1。

## 旧系统缺点

- 单脚本承载采集、标准化、分类、报告、打包，边界不清。
- 只抓 GMGN 有限列表，不是真正全量交易地址。
- 缺少稳定 input/output schema。
- 缺少 `wallet_structure_decision.json`，主系统无法稳定消费。
- 缺少资金边表、Token 流边表、同源组、分发路径、回流路径。
- `native_transfer` 只被写入原始字段，没有展开为边。
- `wallet_age_days`、`first_seen_time`、`last_active_time`、`token_count`、`traded_token_count` 不完整。
- 角色判断依赖单字段/浅标签，证据链不完整。
- GMGN 备注没有结构化字典。
- 历史地址库、跨币复现、多快照复盘机制不稳定。

## 可以保留的部分

- GMGN 拉取命令组合。
- CSV 作为轻量输出格式，不使用 TSV。
- 地址合并与 `source_lists` 概念。
- 早期重点地址优先、低权重地址跳过深挖的成本控制原则。
- 基础设施不进入普通钱包评分但保留关系边的原则。
- E/R/A/I 等级思想。
- 复盘窗口：T+1h/T+6h/T+24h/T+72h/T+7d。
- 单币 Markdown 报告可作为人工复核材料。

## 不应该继续保留的部分

- 不应继续把所有逻辑堆在 `sikk_gmgn_token_report.py`。
- 不应把 `PAPER_READY` 或交易动作写入本模块。
- 不应将 “庄家” 作为确定标签。
- 不应让单字段标签直接 hard block。
- 不应把 dashboard、Telegram 面板、paper runner 逻辑放进钱包模块。
- 不应新增复杂数据库服务；先使用 CSV/JSON/Markdown 文件契约。
