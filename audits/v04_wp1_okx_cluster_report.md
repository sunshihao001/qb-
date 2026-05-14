# SIKK-SOL v0.4 WP1 审计报告：OKX 前300集群字段合约与 fixture analyzer

## 目标

新增只读模块：

```text
sikk_okx_cluster_holding_analyzer.py
```

用于把 OKX 前300 Holder Cluster / 集群关联 / 持仓变化 delta 标准化为 SIKK 可读取的 `okx_cluster_decision.json`。

## 新增能力

- 支持 JSON / CSV fixture 输入。
- 输出单 token 标准合约：
  - `okx_cluster_decision.json`
  - `okx_cluster_groups.csv`
  - `okx_cluster_holding_behavior.csv`
- 输出汇总文件：
  - `okx_cluster_summary.json`
  - `okx_cluster_summary.csv`
  - `okx_cluster_summary.md`
- 缺数据时输出 `OKX_CLUSTER_MISSING`，不崩溃、不卡死主流程。

## 核心字段

```text
okx_cluster_status
okx_cluster_score
okx_cluster_risk_score
okx_cluster_distribution_score
okx_cluster_control_retention_score
okx_cluster_reason
top300_wallet_count
cluster_count
linked_wallet_count
largest_cluster_wallet_count
largest_cluster_holding_pct
top300_total_holding_pct
cluster_total_holding_pct
cluster_sync_buy_score
cluster_sync_sell_score
cluster_holding_pct_delta
cluster_sold_pct_delta
largest_cluster_holding_pct_delta
top300_total_holding_pct_delta
dominant_cluster_role
paper_gate_effect
```

## 状态枚举

```text
CLUSTER_SUPPORT
CLUSTER_CONTROL_HOLDING
CLUSTER_SECOND_STAGE_SUPPORT
CLUSTER_DISTRIBUTION_RISK
CLUSTER_COUNTERPARTY_ABSORBING
CLUSTER_BAGHOLDER_PRESSURE
CLUSTER_NEUTRAL
OKX_CLUSTER_MISSING
```

## 安全边界

- 本模块只读本地输入并写标准化文件。
- 不调用真实交易。
- 不签名。
- 不广播。
- 不调用 `gmgn_swap` / `gmgn_cooking`。
- `SUPPORT_PAPER_ONLY_IF_OTHER_GATES_PASS` 仅表示 paper-only 支持证据，不能绕过 signal/quote/security gates。

## 测试结果

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_okx_cluster_holding_analyzer.py
```

结果：

```text
4 passed in 0.02s
```
