# Wallet-Intel 行为推断交接补充合同

## 目的

本补充合同把 `/root/sikk-wallet-intel/` 中有用的 Behavior-Inference / Wallet-Fact 协同知识吸收到 `/root/sikk-gmgn/` 的 Source Wallet Bot 交接层，作为 `bot2_handoff_packet.json` 的扩展说明，不覆盖原合同。

## 主目录修正

- 钱包结构分析主项目：`/root/sikk-gmgn/`
- 事实输出主路径：`data/source_wallet_bot/<mode>/<token_address>/structure_analysis/wallet_fact/`
- intelligence 输出主路径：`data/source_wallet_bot/<mode>/<token_address>/structure_analysis/intelligence/`
- handoff 输出主路径：`data/source_wallet_bot/<mode>/<token_address>/structure_analysis/handoff/`
- Wallet-Intel 来源：`/root/sikk-wallet-intel/` 只作为协同/推断知识来源。

## Bot2 / 行为推断只允许读取的事实文件

- `wallet_structure_normalized.json`
- `chip_distribution_summary.json`
- `same_source_groups.json`
- `fund_flow_edges.csv`
- `address_history.json`
- `wallet_fact_package_manifest.json`

## 建议新增 handoff sections

这些 section 可以作为 `bot2_handoff_packet.json` 的 future optional extension，不要求旧 schema 立即强制必填：

```json
{
  "behavior_inference_input_refs": [],
  "quantitative_structure_refs": [],
  "counter_evidence_refs": [],
  "missing_fields_for_behavior_inference": [],
  "downgrade_policy": {
    "missing_same_source_confirmation": "downgrade_to_E1_or_E2",
    "missing_backflow_confirmation": "no_high_confidence_distribution_or_exit",
    "missing_inventory_denominator": "do_not_force_inventory_ratio"
  },
  "allowed_behavior_status": [
    "疑似吸筹",
    "疑似控盘",
    "疑似洗盘",
    "疑似突破测试",
    "疑似推进拉升",
    "疑似二段扩张",
    "疑似部分派发",
    "疑似主动派发",
    "疑似撤退",
    "疑似再吸筹",
    "疑似再激活",
    "疑似放弃维护",
    "INSUFFICIENT_DATA",
    "STALE_INPUT"
  ]
}
```

## 禁止交接字段

不得在 Source Wallet Bot 交接包里输出或暗示：

- `PAPER_READY`
- `BLOCKED`
- `final_trade_gate`
- `buy_signal`
- `sell_signal`
- `execute_now`
- `open_position`
- `take_profit`
- `stop_loss`
- `real_execution_action`
- `确定庄家`
- `确定内幕`
- `必拉`
- `必砸`

## 行为推断降级规则

- 没有标准事实文件：输出 `INSUFFICIENT_DATA`。
- 输入快照过旧：输出 `STALE_INPUT`。
- 缺少同源强确认：不能高置信判断主导侧成本区。
- 缺少利润回流/历史复现：不能高置信判断派发完成或撤退。
- 缺少库存 denominator：不得强行计算库存百分比。
- 只有 GMGN 标签：只能作为辅助证据，不能作为同源结论。

## 输出解释报告要求

行为推断报告必须包含：

1. 使用了哪些事实输入。
2. 支持证据。
3. 反证。
4. 缺失字段。
5. 替代假设。
6. 为什么不能更高置信度。
7. 只读结构情报边界声明。
