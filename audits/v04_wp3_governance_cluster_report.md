# SIKK-SOL v0.4 WP3 审计报告：dashboard / audit / explainability 增加 OKX 集群字段

## 目标

让 v0.4 OKX 前300集群证据在治理层可见、可审计、可解释。

## 修改文件

```text
sikk_system_audit.py
sikk_explainability_engine.py
sikk_dashboard_builder.py
tests/test_sikk_system_audit.py
tests/test_sikk_explainability_engine.py
tests/test_sikk_runtime_v02.py
```

## 系统审计增强

新增 v0.4 dashboard 必查字段：

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

审计逻辑会从 `status["okx_cluster"]` 展开字段；缺字段进入 dashboard missing field 统计。

## 解释层增强

解释层新增 OKX 集群证据引用：

- `为什么支持`：引用 `CLUSTER_SUPPORT / CLUSTER_CONTROL_HOLDING / CLUSTER_SECOND_STAGE_SUPPORT`。
- `为什么暂停`：引用 `CLUSTER_COUNTERPARTY_ABSORBING / CLUSTER_BAGHOLDER_PRESSURE`。
- `为什么阻断`：引用 `CLUSTER_DISTRIBUTION_RISK`。
- `下一步看什么`：固定复查 OKX 前300集群状态、支持分、风险分、派发分、控筹保持分。
- `主要失效条件`：加入 OKX 集群转派发风险、同步卖出分升高、最大集群持仓 delta 快速转负。

解释层仍然不重新裁决、不生成交易授权。

## Dashboard 增强

`live_dashboard.html` token 表新增字段：

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

缺字段显示 `待补`。

## 安全边界

- OKX 集群支持不等于买入。
- OKX 集群风险不等于真实卖出。
- dashboard/audit/explainability 全部只读解释，不执行交易。

## 测试结果

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_system_audit.py tests/test_sikk_explainability_engine.py tests/test_sikk_runtime_v02.py
```

结果：

```text
13 passed in 0.08s
```
