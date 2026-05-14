# SIKK-SOL v0.4 工作包拆分

## 总目标

把 v0.3 的 paper-only 筹码控制权状态机升级为 v0.4：

```text
OKX 前300集群关联与持仓行为层
+ 集群状态接入筹码控制权状态机
+ dashboard / audit / explainability 增加 OKX 集群字段
+ 多轮快照 delta 与 paper failure attribution
```

## 全局安全边界

- paper-only。
- 禁止真实买入。
- 禁止真实卖出。
- 禁止调用 `gmgn_swap`。
- 禁止调用 `gmgn_cooking`。
- 禁止交易广播。
- 禁止 `yolo`。
- OKX 集群支持不等于买入；OKX 集群风险不等于真实卖出。
- 缺 OKX 集群数据时降级为 `MISSING/待补`，不得卡死主流程。

## 当前基线

```text
branch=sikk-paper-audit-20260502
baseline=e562a45 feat: add SIKK v0.3 chip control context loop
tests=133 passed in 9.77s
```

## WP1：OKX 前300集群字段合约与 fixture analyzer

目标：新增只读/fixture 驱动模块：

```text
sikk_okx_cluster_holding_analyzer.py
```

输入：

```text
本地 fixture JSON/CSV
未来 OKX Holder Cluster 输出
```

输出：

```text
data/gmgn_candidates_live_run/okx_cluster/<token>/okx_cluster_decision.json
okx_cluster_summary.json
okx_cluster_summary.csv
okx_cluster_summary.md
```

核心字段：

```text
okx_cluster_status
okx_cluster_score
okx_cluster_risk_score
okx_cluster_distribution_score
okx_cluster_control_retention_score
cluster_sync_buy_score
cluster_sync_sell_score
largest_cluster_holding_pct
top300_total_holding_pct
cluster_holding_pct_delta
cluster_sold_pct_delta
largest_cluster_holding_pct_delta
top300_total_holding_pct_delta
```

验收：

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_okx_cluster_holding_analyzer.py
```

## WP2：集群状态接入筹码控制权状态机

目标：让 `sikk_chip_control_state_machine.py` 接收 `okx_cluster_decision` 证据。

规则：

```text
CLUSTER_SUPPORT / CLUSTER_CONTROL_HOLDING / CLUSTER_SECOND_STAGE_SUPPORT
  → 增强 CONTROL_RETAINED_BY_STRUCTURE_SIDE 证据与置信度，但不能绕过其他 gates。

CLUSTER_DISTRIBUTION_RISK / ACTIVE_DISTRIBUTION_CLUSTER
  → 增强 CONTROL_LOST_TO_DISTRIBUTION / BLOCK_OR_FORCE_PAPER_EXIT。

CLUSTER_COUNTERPARTY_ABSORBING / BAGHOLDER_CLUSTER
  → 增强 CONTROL_MIGRATING_TO_COUNTERPARTY / PAUSE_OR_EXIT_MONITOR。

MISSING / NO_CLUSTER_INPUT
  → 只标记 missing_fields，不阻断主流程。
```

验收：

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_chip_control_state_machine.py tests/test_sikk_okx_cluster_holding_analyzer.py
```

## WP3：dashboard / audit / explainability 增加 OKX 集群字段

目标：治理层可见 OKX 集群字段。

修改：

```text
sikk_system_audit.py
sikk_explainability_engine.py
sikk_dashboard_builder.py / sikk_live_run.py（若需要）
```

审计必查字段：

```text
okx_cluster_status
okx_cluster_score
okx_cluster_risk_score
okx_cluster_distribution_score
okx_cluster_control_retention_score
largest_cluster_holding_pct
top300_total_holding_pct
cluster_holding_pct_delta
largest_cluster_holding_pct_delta
```

解释层必须说明：

```text
为什么 OKX 集群支持？
为什么 OKX 集群风险？
是否缺 OKX 集群证据？
OKX 集群如何影响筹码控制权状态？
```

## WP4：多轮快照 delta 与 paper failure attribution

目标：把 OKX 集群 delta 进入 paper 复盘失败归因。

新增/扩展失败类型：

```text
CLUSTER_DISTRIBUTION_RISK
CLUSTER_CONTROL_LOST
CLUSTER_COUNTERPARTY_ABSORBING
CLUSTER_BAGHOLDER_PRESSURE
OKX_CLUSTER_DATA_MISSING
```

验收：

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q
```

最终产物：

```text
audits/v04_wp1_okx_cluster_report.md
audits/v04_wp2_chip_state_cluster_report.md
audits/v04_wp3_governance_cluster_report.md
audits/v04_wp4_failure_attribution_cluster_report.md
```
