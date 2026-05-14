# wallet_structure 模块流程

## 1. 数据接收

接收 token 级输入 JSON，验证 `token_address`、`chain`、`analysis_time`，生成本轮 snapshot id。

## 2. GMGN 拉取

复用旧脚本中的 GMGN 命令组合：token info/security/pool/kline，以及 holders/traders/tagged holders 列表。输出原始快照 `wallet_raw_snapshot.csv`。

## 3. 字段标准化

统一字段别名：`profit/total_profit/pnl`、`buy_volume_cur/buy_volume_usd/total_buy_usd`、`start_holding_at/first_buy_timestamp` 等，输出 `wallet_normalized.csv`。

## 4. 钱包画像

补充或保留 `wallet_age_days`、`first_seen_time`、`last_active_time`、`token_count`、`traded_token_count`、GMGN 标签、历史复现次数。

## 5. 当前代币行为

计算当前 token 内的持仓、买入、卖出、ROI、PNL、清仓、短持、早期参与、高位承接等行为特征。

## 6. Token 来源

将 `transfer_in`、`token_transfer_in`、`token_transfer_out` 展开为 `wallet_token_flow_edges.csv`。缺边时不强判分发。

## 7. 资金来源

将 `native_transfer.from_address`、funding source 字段展开为 `wallet_funding_edges.csv`。区分 CEX/router/pool/program/wallet/unknown。

## 8. 同源组

基于共同 funding source、共同 token source、相近交易时间、相近行为模式形成疑似同源组，输出 `same_source_groups.csv`。单一标签不得构成同源组。

## 9. 分发路径

基于 token source → receiver → sell/transfer out 生成 `distribution_paths.csv`，只输出“疑似分发路径”。

## 10. 回流路径

基于卖出后 native/token 流向共同 sink 或核心资金源生成 `backflow_paths.csv`，只输出“疑似回流”。

## 11. 历史库更新

当 `update_history=true` 且字段质量达标时，将 address profile、role history、review history 写入轻量历史库。失败时不得影响本轮输出。

## 12. GMGN 备注生成

按 `gmgn_note_dictionary.csv` 生成 `gmgn_note_table.csv`。默认只生成备注文件，不自动写回 GMGN。

## 13. wallet_structure_decision.json 输出

`decision_builder` 汇总角色、证据链、风险、支持/暂停/阻断原因，生成主系统可读 JSON。

硬阻断只允许以下结构侧情况：

1. 同源组同步退出。
2. 明显分发卖出。
3. 多地址卖后回流。
4. 早期结构钱包集中清仓。
5. 接盘鲸鱼高位承接明显。
6. 当前钱包结构和盘型冲突。
7. 结构侧筹码明显失控。
8. 历史高风险地址复现。

不能因为单个新钱包、单个 transfer_in、单个 bundler 标签直接 block。
